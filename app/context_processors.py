from app.views import BEST_MEMBERS
from app.models import Tag, BestUser
from WebQA.settings import IS_AUTHORIZED


def tags_context(request):
    top_tags = Tag.objects.get_top_tags()
    top_tags = top_tags.values_list('tag_name', flat=True)

    if len(top_tags) > 8:
        top_tags = top_tags[:8]
    return {'tags': list(top_tags)}


def best_members_context(request):
    best_members_profiles = BestUser.objects.all().select_related('profile__user').values_list(
        'profile__user__username', flat=True)

    best_members_nicks = list(best_members_profiles)

    return {'best_members': best_members_nicks}


def is_authorized(request):
    return {'is_authorized': IS_AUTHORIZED}
