from django.contrib import admin
from .models import ReddemCommunity, ReddemCommunityMembers, Post, Comment, UpvotesAndDownvotesPosts


@admin.register(ReddemCommunity)
class ReddemCommunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']
    search_fields = ['title']
    list_filter = ['owner']


@admin.register(ReddemCommunityMembers)
class ReddemCommunityMembersAdmin(admin.ModelAdmin):
    list_display = ['user', 'community']
    search_fields = ['user__username', 'community__title']
    list_filter = ['user', 'community']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'community', 'owner', 'date_made']
    search_fields = ['title', 'owner__username', 'community__title']
    list_filter = ['community', 'owner']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'commented_post', 'owner', 'date_made']
    search_fields = ['comment', 'owner__username']
    list_filter = ['commented_post', 'owner']


@admin.register(UpvotesAndDownvotesPosts)
class UpvotesAndDownvotesPostsAdmin(admin.ModelAdmin):
    list_display = ['display_vote', 'voted_post', 'owner']
    search_fields = ['owner__username']
    list_filter = ['voted_post', 'owner']

    def display_vote(self, obj):
        return 'Upvote' if obj.vote == 1 else 'Downvote'

    display_vote.short_description = 'Vote'
