from django import forms

from apps.forumApp import models


class ReddemCommunityForm(forms.ModelForm):
    class Meta:
        model = models.ReddemCommunity
        fields = ('image', 'title')


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('community', 'title', 'image', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('user', None)

        if self.user:
            self.fields['community'].queryset = models.UserJoinedCommunities.objects.filter(user=self.user)
