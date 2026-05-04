from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.cars.models import Favorite


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('listing').prefetch_related('listing__photos')
    context = {
        'favorites': favorites,
        'seo_title': 'Избранное - ALAY AVTO 777',
        'seo_description': 'Список избранных объявлений пользователя.',
    }
    return render(request, 'favorites/list.html', context)
