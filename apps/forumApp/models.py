from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from custom_code import custom_mixins

User = get_user_model()


class ReddemCommunity(custom_mixins.GetAbsoluteUrlMixin, models.Model):

    class Meta:
        verbose_name_plural = 'Reddem communities'

    image = models.ImageField(
        upload_to='CommunityImages'
    )

    title = models.CharField(
        max_length=20,
        unique=True,
    )

    owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owner'
    )

    slug = AutoSlugField(
        populate_from='title'
    )

    members = models.ManyToManyField(
        to=User,
        through='ReddemCommunityMembers'
    )

    def pk_and_slug_url_kwargs(self):
        return {'slug_community': self.slug}

    def home_community_absolute_url(self):
        return self.get_absolute_url('home community', self.pk_and_slug_url_kwargs())

    def edit_community_absolute_url(self):
        return self.get_absolute_url('edit community', self.pk_and_slug_url_kwargs())

    def join_community_absolute_url(self):
        return self.get_absolute_url('join community', self.pk_and_slug_url_kwargs())

    def leave_community_absolute_url(self):
        return self.get_absolute_url('leave community', self.pk_and_slug_url_kwargs())

    def __str__(self):
        return 'Community'


class ReddemCommunityMembers(models.Model):

    class Meta:
        verbose_name_plural = 'Reddem community members'

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    community = models.ForeignKey(
        to=ReddemCommunity,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return 'Community member'


# Create your models here.
class Post(custom_mixins.GetAbsoluteUrlMixin, models.Model):
    community = models.ForeignKey(
        to=ReddemCommunity,
        on_delete=models.SET_NULL,
        null=True
    )

    title = models.CharField(
        max_length=50
    )

    image = models.ImageField(
        upload_to='PostImages',
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    slug = AutoSlugField(
        populate_from='title'
    )

    date_made = models.DateTimeField(auto_now_add=True)

    def pk_and_slug_url_kwargs(self):
        return {'pk_post': self.pk, 'slug_post': self.slug}

    def details_post_absolute_url(self):
        kwargs = ReddemCommunity.pk_and_slug_url_kwargs(self.community)

        kwargs.update(self.pk_and_slug_url_kwargs())

        return self.get_absolute_url('details post', kwargs)

    def upvote_post_absolute_url(self):
        kwargs = ReddemCommunity.pk_and_slug_url_kwargs(self.community)

        kwargs.update(self.pk_and_slug_url_kwargs())

        return self.get_absolute_url('upvote post', kwargs)

    def downvote_post_absolute_url(self):
        kwargs = ReddemCommunity.pk_and_slug_url_kwargs(self.community)

        kwargs.update(self.pk_and_slug_url_kwargs())

        return self.get_absolute_url('downvote post', kwargs)

    def delete_post_absolute_url(self):
        kwargs = ReddemCommunity.pk_and_slug_url_kwargs(self.community)

        kwargs.update(self.pk_and_slug_url_kwargs())

        return self.get_absolute_url('delete post', kwargs)

    def __str__(self):
        return 'Post'


class Comment(models.Model):
    comment = models.CharField(
        max_length=300,
    )

    commented_post = models.ForeignKey(
        to=Post,
        on_delete=models.SET_NULL,
        null=True
    )

    owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True
    )

    date_made = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment'


class UpvotesAndDownvotesPosts(models.Model):

    class Meta:
        verbose_name_plural = 'Upvotes and downvotes - posts'

    vote = models.IntegerField()

    voted_post = models.ForeignKey(
        to=Post,
        on_delete=models.SET_NULL,
        null=True
    )

    owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return 'Upvote' if self.vote == 1 else 'Downvote'
