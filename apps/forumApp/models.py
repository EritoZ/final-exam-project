from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ReddemCommunity(models.Model):
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
        null=True
    )

    slug = AutoSlugField(
        populate_from='title'
    )

    def __str__(self):
        return self.title


class UserJoinedCommunities(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    community = models.ForeignKey(
        to=ReddemCommunity,
        on_delete=models.CASCADE
    )


# Create your models here.
class Post(models.Model):
    community = models.ForeignKey(
        to=UserJoinedCommunities,
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
