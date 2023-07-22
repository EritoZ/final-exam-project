from django.contrib.auth import get_user_model, mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.forumApp import models, forms
from custom_code import custom_mixins

User = get_user_model()


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            joined_community_posts = models.Post.objects \
                .filter(community__userjoinedcommunities__user=self.request.user)

            kwargs['community_posts'] = joined_community_posts.order_by('-id')
        else:
            kwargs['community_posts'] = models.Post.objects.all().order_by('-id')

        return super().get_context_data(**kwargs)


@login_required
def create_post(request):
    form = forms.CreatePostForm(request.POST or None, request.FILES or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.instance.owner = request.user
        print(form.instance.image)
        form.save()
        return redirect('index')

    return render(request, 'posts/create-post-page.html', context={'form': form})


class CommunityCreateView(mixins.LoginRequiredMixin, custom_mixins.OwnerAddMixin, generic.CreateView):
    template_name = 'communities/create-community-page.html'
    model = models.ReddemCommunity
    form_class = forms.ReddemCommunityForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        models.UserJoinedCommunities.objects.create(community=self.object, user=self.request.user)

        return result


class CommunityHomeView(generic.DetailView):
    template_name = 'communities/home-community-page.html'
    model = models.ReddemCommunity

    def get_context_data(self, **kwargs):
        kwargs['posts'] = models.Post.objects.filter(slug=self.object.slug).order_by('-id')
        kwargs['user_joined'] = models.UserJoinedCommunities.objects.filter(user=self.request.user,
                                                                            community=self.object).exists()
        return super().get_context_data(**kwargs)
