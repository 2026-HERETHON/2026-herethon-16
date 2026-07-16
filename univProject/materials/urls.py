from django.urls import path
from . import views
from curriculums.views import material_bookmark_toggle

urlpatterns = [
    path('', views.material_list_view, name='material_list'),
]
