from django.urls import path, include

from apps.forumApp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.CommunitySearchView.as_view(), name='search community'),
    path('create-community', views.CommunityCreateView.as_view(), name='create community'),
    path('r/<slug:slug_community>/', include([
        path('', views.CommunityHomeView.as_view(), name='home community'),
        path('edit', views.CommunityEditView.as_view(), name='edit community'),
        path('join', views.community_join, name='join community'),
        path('leave', views.community_leave, name='leave community'),

        path('<int:pk_post>/<slug:slug_post>/', include([
            path('comments', views.PostDetailsAndCommentsView.as_view(), name='details post'),
            path('upvote', views.upvote, name='upvote post'),
            path('downvote', views.downvote, name='downvote post'),
            path('delete', views.PostDeleteView.as_view(), name='delete post')
        ]))
    ])),
    path('comment/<int:pk>/', include([
        path('delete', views.CommentDeleteView.as_view(), name='delete comment'),
    ])),
    path('submit', views.create_post, name='submit post'),
]

