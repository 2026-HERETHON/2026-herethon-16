from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [    
    path('signup/', views.signUp, name='signUp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('intro/', views.intro, name='intro'),
    path('landing/', views.landing, name='landing'),
    path('main/', views.main, name='main'),
]