from rest_framework import viewsets
from quizzes.models import Quiz, Question, Answer, UserQuizResult
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, UserQuizResultSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class UserQuizResultViewSet(viewsets.ModelViewSet):
    queryset = UserQuizResult.objects.all()
    serializer_class = UserQuizResultSerializer
