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

    def __str__(self):
        return self.title


class ReddemCommunityMembers(models.Model):
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


class LikesAndDislikes(models.Model):
    liked = models.BooleanField()

    liked_post = models.ForeignKey(
        to=Post,
        on_delete=models.SET_NULL,
        null=True
    )

    owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True
    )
