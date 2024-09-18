# mindquest/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from quizzes import views as quiz_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', quiz_views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', quiz_views.quiz_detail, name='quiz_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', quiz_views.sign_out, name='logout'),
    path('accounts/register/', quiz_views.register, name='register'),
    path('quizzes/', quiz_views.quizzes_view, name='quizzes_view'),
    path('profile/', quiz_views.profile, name='profile'),
    path('setting/', quiz_views.setting, name='setting'),
    path('dashboard/', quiz_views.dashboard, name='dashboard'),
    path('api/', include('rest_api.urls')), 
]
