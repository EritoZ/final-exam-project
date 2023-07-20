from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic

from apps.forumApp import models

User = get_user_model()


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'common/index.html'
    model = models.Post
    context_object_name = 'posts'


class PostCreateView(generic.CreateView):
    template_name = 'accounts/register-page.html'
    model = models.Post
    # form_class =
