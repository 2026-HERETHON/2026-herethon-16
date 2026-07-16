from django.urls import path
from . import views

urlpatterns = [
    path('', views.material_list_view, name='material_list'),
]