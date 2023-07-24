from django import forms

from apps.forumApp import models


class BaseMeta:
    model = ...
    fields = ...


class ReddemCommunityForm(forms.ModelForm):
    class Meta(BaseMeta):
        model = models.ReddemCommunity
        fields = ('image', 'title')


class CreatePostForm(forms.ModelForm):
    class Meta(BaseMeta):
        model = models.Post
        fields = ('community', 'title', 'image', 'description')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = models.ReddemCommunity.objects\
            .filter(reddemcommunitymembers__user=self.user)


class CreateCommentForm(forms.ModelForm):
    class Meta(BaseMeta):
        model = models.Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your thoughts.'
            })
        }
