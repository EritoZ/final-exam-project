from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth import models as auth_models
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages

from apps.accounts import forms
from apps.accounts.tasks import send_email
from apps.forumApp import models as forum_models
from custom_code import custom_mixins

User = get_user_model()


# Create your views here.

class BaseProfileView:
    model = User


class RegisterView(generic.CreateView):
    template_name = 'account/register-page.html'
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.is_active = False
        result = super().form_valid(form)

        auth_models.Group.objects.get(name='regular_user_group').user_set.add(self.object)

        token = default_token_generator.make_token(self.object)
        url = self.request.build_absolute_uri(
            f"{reverse_lazy('email confirmation', kwargs={'pk': self.object.id, 'token': token})}"
        )

        send_email.delay(url, self.object.id)
        messages.success(self.request, 'Check your email for a confirmation mail.')

        return result


# TODO: Make token to be one time use
def email_confirmation(request, pk, token):
    try:

        user = User.objects.get(id=pk)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account made successfully!')
            return redirect('login')

    except User.DoesNotExist:
        pass

    messages.error(request, 'Confirmation link is invalid.')
    return redirect('index')


class LoginView(auth_views.LoginView):
    template_name = 'account/login-page.html'


class LogoutView(auth_views.LogoutView):
    pass


class ProfileDetailsView(BaseProfileView, custom_mixins.VotesContextMixin, generic.DetailView):
    template_name = 'account/details-profile-page.html'

    def get_context_data(self, **kwargs):
        kwargs['posts'] = forum_models.Post.objects.filter(owner=self.object)
        kwargs['user_can_change_user'] = self.request.user.has_perm('Can change user')

        mixin_result = super().get_context_data(**kwargs)

        posts = tuple(mixin_result.get('posts')[:8])
        total_karma = sum(post.points_count for post in posts)
        comments = tuple(forum_models.Comment.objects.filter(owner=self.object)[:8])

        user_posts_and_comments = sorted(posts + comments, key=lambda x: (x.date_made, x.id), reverse=True)

        mixin_result.update({'user_posts_and_comments': user_posts_and_comments, 'total_karma': total_karma})

        return mixin_result


class ProfileEditView(custom_mixins.DataAccessControlMixin, BaseProfileView, generic.UpdateView):
    template_name = 'account/edit-profile-page.html'
    form_class = forms.UserEditForm
    permission_required = ('Can change user',)

    def get_success_url(self):
        return reverse('profile details', kwargs={'slug': self.object.slug})


class ProfileChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'account/change-password-page.html'
    form_class = forms.UserPasswordChangeForm
    permission_required = ('Can change user',)

    def get_success_url(self):
        messages.success(self.request, 'Successfully changed password')

        return reverse('profile details', kwargs={'slug': self.request.user.slug})
