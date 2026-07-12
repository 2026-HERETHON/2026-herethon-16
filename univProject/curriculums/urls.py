from django.urls import path
from . import views

urlpatterns = [
    path('my-major/', views.my_major_view, name='my_major'),
]