from abc import abstractmethod

from django.urls import reverse
from django.db import models as aggregate

from apps.forumApp import models


class OwnerAddMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class VotesContextMixin:

    def get_context_data(self, **kwargs):

        if 'posts' in kwargs:
            for post in kwargs['posts']:
                upvotes = models.UpvotesAndDownvotesPosts.objects.filter(vote=1, voted_post=post)
                downvotes = models.UpvotesAndDownvotesPosts.objects.filter(vote=0, voted_post=post)

                post.upvoted = upvotes.filter(owner=self.request.user.pk).exists()
                post.downvoted = downvotes.filter(owner=self.request.user.pk).exists()

                post.points_count = upvotes.count() - downvotes.count()

        return super().get_context_data(**kwargs)


class GetAbsoluteUrlMixin:

    @abstractmethod
    def pk_and_slug_url_kwargs(self):
        ...

    def get_absolute_url(self, view, kwargs):
        return reverse(view, kwargs=kwargs)
