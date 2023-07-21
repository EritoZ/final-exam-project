from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy
from django.views import generic

from apps.forumApp import models, forms
from custom_code import custom_mixins

User = get_user_model()


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        joined_community_posts = models.Post.objects.none()

        for community in models.UserJoinedCommunities.objects.filter(user=self.request.user):
            joined_community_posts | models.Post.objects.filter(community=community)
            
        kwargs['joined_community_posts'] = joined_community_posts.order_by('-id')
        
        return super().get_context_data(**kwargs)


def create_post(request):

    if request.method == 'POST':
        form = forms.CreatePostForm(request.POST, user=request.user)
        # if form.is_valid():
        #     return form_valid(form)
        # else:
        #     return form_invalid(form)
    #
    # else:



class CommunityCreateView(mixins.LoginRequiredMixin, custom_mixins.OwnerAddMixin, generic.CreateView):
    template_name = 'communities/create-community-page.html'
    model = models.ReddemCommunity
    form_class = forms.ReddemCommunityForm
    success_url = reverse_lazy('index')


class CommunityHomeView(generic.DetailView):
    template_name = 'communities/home-community-page.html'
    model = models.ReddemCommunity

    def get_context_data(self, **kwargs):
        kwargs['posts'] = models.Post.objects.filter(slug=self.object.slug).order_by('-id')
        kwargs['user_joined'] = models.UserJoinedCommunities.objects.filter(user=self.request.user,
                                                                            community=self.object).exists()
        return super().get_context_data(**kwargs)
