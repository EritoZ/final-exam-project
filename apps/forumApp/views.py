from django.contrib.auth import get_user_model, mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from apps.forumApp import models, forms
from custom_code import custom_mixins

User = get_user_model()


class BasePostView:
    model = models.Post
    pk_url_kwarg = 'pk_post'
    slug_url_kwarg = 'slug_post'


class BaseCommunityView:
    model = models.ReddemCommunity
    slug_url_kwarg = 'slug_community'


# Create your views here.
class IndexView(custom_mixins.ReactionsContextMixin, generic.TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            joined_community_posts = models.Post.objects \
                .filter(community__reddemcommunitymembers__user=self.request.user)

            kwargs['community_posts'] = joined_community_posts.order_by('-id')

        else:
            kwargs['community_posts'] = models.Post.objects.all().order_by('-id')

        return super().get_context_data(**kwargs)


@login_required
def create_post(request):
    form = forms.CreatePostForm(request.POST or None, request.FILES or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.instance.owner = request.user
        form.save()

        models.LikesAndDislikes.objects.create(liked=True, liked_post=form.instance, owner=request.user)

        return redirect('index')

    return render(request, 'posts/create-post-page.html', context={'form': form})


class PostDetailsAndCommentsView(BasePostView, generic.DetailView):
    template_name = 'posts/details-post-page.html'

    def get_context_data(self, **kwargs):
        likes = models.LikesAndDislikes.objects.filter(liked=True, liked_post=self.object)
        dislikes = models.LikesAndDislikes.objects.filter(liked=False, liked_post=self.object)

        kwargs['liked'] = likes.filter(owner=self.request.user.pk)
        kwargs['disliked'] = dislikes.filter(owner=self.request.user.pk)

        kwargs['likes_and_dislikes_count'] = likes.count() - dislikes.count()

        kwargs['form'] = forms.CreateCommentForm()

        post_comments = models.Comment.objects.filter(commented_post=self.object)

        kwargs['post_comments'] = post_comments.order_by('-id')
        kwargs['post_comments_amount'] = post_comments.count()

        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.CreateCommentForm(request.POST)

        if form.is_valid():
            form.instance.commented_post = self.get_object()
            form.instance.owner = self.request.user
            form.save()

            return redirect('details post',
                            slug_community=self.kwargs['slug_community'], slug_post=self.kwargs['slug_post'])

        return render(request, self.template_name)


class PostDeleteView(BasePostView, generic.DeleteView):
    template_name = 'posts/delete-post-page.html'

    def get_success_url(self):
        return reverse('profile details', kwargs={'slug': self.request.user.slug})


class CommunityCreateView(mixins.LoginRequiredMixin, custom_mixins.OwnerAddMixin, generic.CreateView):
    template_name = 'communities/create-community-page.html'
    model = BaseCommunityView.model
    form_class = forms.CreateReddemCommunityForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        models.ReddemCommunityMembers.objects.create(community=self.object, user=self.request.user)

        return result


class CommunitySearchView(BaseCommunityView, generic.ListView):
    template_name = 'communities/search-community-page.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', None)

        queryset = queryset.filter(title__icontains=search)

        return queryset


class CommunityHomeView(BaseCommunityView, custom_mixins.ReactionsContextMixin, generic.DetailView):
    template_name = 'communities/home-community-page.html'

    def get_context_data(self, **kwargs):
        kwargs['community_posts'] = models.Post.objects.filter(community=self.object).order_by('-id')

        kwargs['user_joined'] = models.ReddemCommunityMembers.objects.filter(user=self.request.user.pk,
                                                                             community=self.object).exists()

        kwargs['members_count'] = models.ReddemCommunityMembers.objects.filter(community=self.object).count()

        return super().get_context_data(**kwargs)


class CommunityEditView(BaseCommunityView, generic.UpdateView):
    template_name = 'communities/edit-community-page.html'
    form_class = forms.EditReddemCommunityForm

    def get_success_url(self):
        return self.model.home_community_absolute_url(self.object)


@login_required
def community_join(request, slug_community):
    current_community = get_object_or_404(klass=models.ReddemCommunity, pk=slug_community)
    models.ReddemCommunityMembers.objects.create(community=current_community, user=request.user)

    return redirect('home community', slug_community=slug_community)


def community_leave(request, slug_community):
    current_community = get_object_or_404(klass=models.ReddemCommunity, pk=slug_community)
    models.ReddemCommunityMembers.objects.filter(community=current_community, user=request.user.pk).delete()

    return redirect('home community', slug_community=slug_community)


@login_required
def like(request, pk_post, slug_community, slug_post):
    return react(request, pk_post, True)


@login_required
def dislike(request, pk_post, slug_community, slug_post):
    return react(request, pk_post, False)


def react(request, pk_post, liked: bool):
    found_post = models.Post.objects.get(pk=pk_post)

    found_reaction = models.LikesAndDislikes.objects.filter(liked_post=found_post, owner=request.user)

    previous_page = request.META.get('HTTP_REFERER')

    try:
        found_reaction = found_reaction.get()

        if found_reaction.liked == liked:
            found_reaction.delete()

        else:
            found_reaction.liked = liked
            found_reaction.save()

    except models.LikesAndDislikes.DoesNotExist:
        models.LikesAndDislikes.objects.create(liked=liked, liked_post=found_post, owner=request.user)

    if previous_page:
        return redirect(previous_page)

    return redirect('index')
