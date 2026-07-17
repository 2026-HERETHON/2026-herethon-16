from django.urls import path
from . import views

urlpatterns = [
    path('my-major/', views.my_major_view, name='my_major'),
    path('lesson/<int:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
    path('lesson/<int:lesson_id>/complete/', views.lesson_complete_view, name='lesson_complete'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('bookmarked-materials/', views.bookmarked_materials_view, name='bookmarked_materials'),
]