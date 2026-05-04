import json
from django.views.generic import TemplateView
from apps.cars.models import CarListing, Favorite, MAKE_CHOICES, MODELS_BY_MAKE


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = CarListing.objects.filter(status='active', is_featured=True).prefetch_related('photos')[:6]
        context['latest'] = CarListing.objects.filter(status='active').prefetch_related('photos')[:12]
        if self.request.user.is_authenticated:
            context['favorite_ids'] = set(Favorite.objects.filter(user=self.request.user).values_list('listing_id', flat=True))
        else:
            context['favorite_ids'] = set()
        context['listings_count'] = CarListing.objects.filter(status='active').count()
        context['make_choices'] = MAKE_CHOICES
        context['models_by_make_json'] = json.dumps(MODELS_BY_MAKE, ensure_ascii=False)
        context['seo_title'] = 'ALAY AVTO 777 - Продажа авто в Бишкеке'
        context['seo_description'] = 'Автосалон ALAY AVTO 777: авто из Кореи, рассрочка, Trade-In. Бишкек, Кыргызстан.'
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
