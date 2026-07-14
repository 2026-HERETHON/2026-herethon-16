from django.urls import path
from . import views

urlpatterns = [
    path('', views.material_list_view, name='material_list'),
    path('bookmarked/', views.bookmarked_materials_view, name='bookmarked_materials'),
    path('<int:material_id>/bookmark/', views.material_bookmark_toggle, name='material_bookmark_toggle'),
]