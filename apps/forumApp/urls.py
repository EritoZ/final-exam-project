from django.urls import path, include

from apps.forumApp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('r/', include([

        path('create', views.CommunityCreateView.as_view(), name='create community'),

        path('<slug:slug_community>/', include([

            path('', views.CommunityHomeView.as_view(), name='home community'),
            path('join', views.community_join, name='join community'),
            path('leave', views.community_leave, name='leave community'),
            path('comments/<slug:slug_post>', views.PostDetailsView.as_view(), name='details post'),

        ])),
    ])),
    path('submit', views.create_post, name='submit post'),
]