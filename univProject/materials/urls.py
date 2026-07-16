from django.urls import path
from . import views
from curriculums.views import material_bookmark_toggle

urlpatterns = [
    path('', views.material_list_view, name='material_list'),
<<<<<<< HEAD
    path('<int:material_id>/bookmark/', material_bookmark_toggle, name='material_bookmark_toggle'),
]
=======
]
>>>>>>> 5744863f0f42ff486eca75feee5150eae4129576
