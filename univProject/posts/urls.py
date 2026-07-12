from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.post_like, name='post_like'),
    path('<int:post_id>/cheer/', views.post_cheer, name='post_cheer'),
    path('<int:post_id>/comment/', views.comment_create, name='comment_create'),
]