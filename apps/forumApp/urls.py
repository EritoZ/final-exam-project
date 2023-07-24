from django.urls import path, include

from apps.forumApp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create-communtiy', views.CommunityCreateView.as_view(), name='create community'),
    path('r/<slug:slug_community>/', include([
        path('', views.CommunityHomeView.as_view(), name='home community'),
        path('join', views.community_join, name='join community'),
        path('leave', views.community_leave, name='leave community'),

        path('<slug:slug_post>/', include([
            path('comments', views.PostDetailsAndCommentsView.as_view(), name='details post'),
            # TODO: Make like
            # path('like', views.find_emotion, name='like post')
        ]))
    ])),
    path('submit', views.create_post, name='submit post'),
]
