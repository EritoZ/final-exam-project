from abc import abstractmethod

from django.contrib.auth import mixins
from django.urls import reverse
from django.db import models as aggregate

from apps.forumApp import models


class OwnerAddMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class DataAccessControlMixin(mixins.UserPassesTestMixin):
    permission_required = (None,)

    def test_func(self):
        """
        You can modify this func based on your needs.
        :return:
        """

        if not self.request.user.is_authenticated:
            return False

        obj = self.get_object()

        if hasattr(obj, 'owner'):
            obj = obj.owner

        return self.request.user == obj or self.request.user.has_perms(self.permission_required)


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
