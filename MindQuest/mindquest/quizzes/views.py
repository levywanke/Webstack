from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, Question, Answer, UserQuizResult
from django.db.models import Sum
# quizzes/views.py
from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Answer

@login_required
def dashboard(request):
    # Calculate overall user progress
    user_quiz_results = UserQuizResult.objects.filter(user=request.user)
    total_score = user_quiz_results.aggregate(total_score=Sum('score'))['total_score'] or 0
    total_quizzes = user_quiz_results.count()
    progress_percentage = (total_score / (total_quizzes * 10)) * 100 if total_quizzes else 0

    # Define the grade based on progress percentage
    if progress_percentage >= 80:
        grade = "A"
    elif progress_percentage >= 60:
        grade = "B"
    elif progress_percentage >= 40:
        grade = "C"
    elif progress_percentage >= 20:
        grade = "D"
    else:
        grade = "E"

    # Retrieve top performers (or any other relevant data)
    top_performers = UserQuizResult.objects.order_by('-score')[:10]

    context = {
        'progress_percentage': progress_percentage,
        'grade': grade,
        'top_performers': top_performers
    }
    return render(request, 'quizzes/quiz_list.html', context)




def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

from django.contrib import messages

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    score = None
    percentage = None
    total_questions = questions.count()
    progress_percentage = 0
    performance_message = ""
    grade = ""

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = get_object_or_404(Answer, id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        progress_percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        # Define performance messages based on score
        if percentage >= 80:
            performance_message = "Excellent!"
            grade = "A"
        elif percentage >= 60:
            performance_message = "Good job!"
            grade = "B"
        elif percentage >= 40:
            performance_message = "Fair attempt!"
            grade = "C"
        elif percentage >= 20:
            performance_message = "Needs improvement!"
            grade = "D"
        else:
            performance_message = "Keep practicing!"
            grade = "E"

        # Save or update quiz results
        UserQuizResult.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score}
        )

    # Calculate overall user progress
    user_quiz_results = UserQuizResult.objects.filter(user=request.user)
    total_score = user_quiz_results.aggregate(total_score=Sum('score'))['total_score'] or 0
    total_quizzes = user_quiz_results.count()
    progress_percentage = (total_score / (total_quizzes * 10)) * 100 if total_quizzes else 0

    context = {
        'quiz': quiz,
        'questions': questions,
        'score': score,
        'percentage': percentage,
        'total_questions': total_questions,
        'progress_percentage': progress_percentage,
        'performance_message': performance_message,
        'grade': grade
    }
    return render(request, 'quizzes/quiz_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('quiz_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('quiz_list')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def quizzes_view(request):
    user = request.user
    
    # Retrieve current score and quizzes completed
    current_score = UserQuizResult.objects.filter(user=user).aggregate(total_score=sum('score'))['total_score'] or 0
    quizzes_completed = UserQuizResult.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'current_score': current_score,
        'quizzes_completed': quizzes_completed,
        'quizzes': Quiz.objects.all(),  # Retrieve quizzes as needed
    }
    
    return render(request, 'quizzes/quiz_list.html', context)



def profile(request):
    # Fetch user-specific data and pass it to the template
    return render(request, 'quizzes/profile.html')



def sign_out(request):
    logout(request)
    return redirect('login') 


@login_required
def setting(request):
    user = request.user
    # Process settings update if form is submitted
    if request.method == 'POST':
        # Handle form submission and update user settings
        pass
    return render(request, 'quizzes/settings.html', {'user': user})



import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Initialize OpenAI API client
openai.api_key = settings.OPENAI_API_KEY

@require_GET
def get_recommendations(request):
    try:
        # Call OpenAI API to get recommendations
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Provide a list of recommended topics based on user interests.",
            max_tokens=150
        )
        recommendations = response.choices[0].text.strip().split('\n')

        return JsonResponse({'recommendations': recommendations})
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return JsonResponse({'recommendations': []}, status=500)
