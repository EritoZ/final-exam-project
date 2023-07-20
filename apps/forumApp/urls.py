from django.urls import path

from apps.forumApp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]