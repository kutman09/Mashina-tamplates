from apps.cars.models import Favorite


def favorites_count(request):
    if request.user.is_authenticated:
        return {'favorites_count': Favorite.objects.filter(user=request.user).count()}
    return {'favorites_count': 0}
