from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=50
    )

    image = models.ImageField(
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
