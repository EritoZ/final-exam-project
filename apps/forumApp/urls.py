from django.urls import path, include

from apps.forumApp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('r/', include([
        path('create', views.CommunityCreateView.as_view(), name='create community'),
        path('<slug:slug>/', views.CommunityHomeView.as_view(), name='home community'),
    ])),
    path('submit', views.create_post, name='submit post'),
]