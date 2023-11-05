from app.views import TAGS, BEST_MEMBERS, IS_AUTHORIZED


def tags_context(request):
    return {'tags': TAGS}


def best_members_context(request):
    return {'best_members': BEST_MEMBERS}


def is_authorized(request):
    return {'is_authorized': IS_AUTHORIZED}
