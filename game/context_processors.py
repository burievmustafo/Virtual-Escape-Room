from .models import UserProfile


def user_profile(request):
    if not request.user.is_authenticated:
        return {}

    profile = getattr(request.user, 'profile', None)
    if profile is None:
        profile = UserProfile.objects.create(user=request.user)
    return {'user_profile': profile}
