from django.urls import path
from . import views
from curriculums.views import material_bookmark_toggle

urlpatterns = [
    path('', views.material_list_view, name='material_list'),
    path('<int:material_id>/bookmark/', material_bookmark_toggle, name='material_bookmark_toggle'),
]
