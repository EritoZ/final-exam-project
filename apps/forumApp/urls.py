from django.urls import path, include

from apps.forumApp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.CommunitySearchView.as_view(), name='search community'),
    path('create-communtiy', views.CommunityCreateView.as_view(), name='create community'),
    path('r/<slug:slug_community>/', include([
        path('', views.CommunityHomeView.as_view(), name='home community'),
        path('edit', views.CommunityEditView.as_view(), name='edit community'),
        path('join', views.community_join, name='join community'),
        path('leave', views.community_leave, name='leave community'),

        path('<int:pk_post>/<slug:slug_post>/', include([
            path('comments', views.PostDetailsAndCommentsView.as_view(), name='details post'),
            path('like', views.like, name='like post'),
            path('dislike', views.dislike, name='dislike post'),
            path('delete', views.PostDeleteView.as_view(), name='delete post')
        ]))
    ])),
    path('submit', views.create_post, name='submit post'),
]

