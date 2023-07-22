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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = models.ReddemCommunity.objects.filter(userjoinedcommunities__user=self.user)
