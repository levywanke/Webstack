# quizzes/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/', views.quizzes_view, name='quizzes_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.sign_out, name='logout'),
    path('settings/', views.settings, name='settings'),
     path('api/recommendations/', views.get_recommendations, name='get_recommendations'),
]

