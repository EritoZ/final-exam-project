from abc import abstractmethod

from django.urls import reverse

from apps.forumApp import models


class OwnerAddMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class ReactionsContextMixin:

    def get_context_data(self, **kwargs):
        for post in kwargs['community_posts']:
            likes = models.LikesAndDislikes.objects.filter(liked=True, liked_post=post)
            dislikes = models.LikesAndDislikes.objects.filter(liked=False, liked_post=post)

            post.liked = likes.filter(owner=self.request.user.pk)
            post.disliked = dislikes.filter(owner=self.request.user.pk)

            post.likes_and_dislikes_count = likes.count() - dislikes.count()

        return super().get_context_data(**kwargs)


class GetAbsoluteUrlMixin:

    @abstractmethod
    def pk_and_slug_url_kwargs(self):
        ...

    def get_absolute_url(self, view, kwargs):
        return reverse(view, kwargs=kwargs)