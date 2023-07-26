from apps.forumApp import models


def joined_communities_by_user(request):
    context = {
        'joined_communities': models.ReddemCommunity.objects \
            .filter(reddemcommunitymembers__user=request.user.pk).order_by('title')
    }

    return context
