from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.cars.models import Favorite


@login_required
def profile(request):
    listings = request.user.listings.prefetch_related('photos')
    context = {
        'listings': listings,
        'active_count': listings.filter(status='active').count(),
        'sold_count': listings.filter(status='sold').count(),
        'fav_count': Favorite.objects.filter(user=request.user).count(),
        'seo_title': 'Мой профиль - ALAY AVTO 777',
        'seo_description': 'Личный кабинет продавца и статистика объявлений.',
    }
    return render(request, 'accounts/profile.html', context)
