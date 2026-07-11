from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.list, name='list'), 
    path('create/', views.create, name='create'), 
    path('<int:id>/', views.detail, name='detail'), 
    path('<int:id>/update/', views.update, name='update'), 
    path('<int:id>/delete/', views.delete, name='delete'), 
    path('result/', views.result, name='result'), 
    path('<int:id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:id>/like/', views.post_like, name='post_like'),
]