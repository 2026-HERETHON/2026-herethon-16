from django.urls import path
from . import views

urlpatterns = [
    path("", views.intro, name="intro"),
    path("select1/", views.select1, name="select1"),
    path("select2/", views.select2, name="select2"),
    path("select3/", views.select3, name="select3"),
    path("loading/", views.loading, name="loading"),
    path('submitAnswer/', views.submitAnswer, name='submitAnswer'),
    path('resultView/', views.resultView, name='confirm'),

    path("recommend1/", views.recommend1, name="recommend1"),
    path("experience1/", views.experience1, name="experience1"),
    path("recommend2/", views.recommend2, name="recommend2"),
    path("experience2/", views.experience2, name="experience2"),
    path("confirm/", views.confirm, name="confirm"),
]
