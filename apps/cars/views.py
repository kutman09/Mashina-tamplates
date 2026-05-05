from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from slugify import slugify
from .filters import CarFilter
from .forms import CarListingForm
from .models import CarListing, CarPhoto, Favorite, MODELS_BY_MAKE


class CarListView(ListView):
    model = CarListing
    template_name = 'cars/list.html'
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        queryset = CarListing.objects.filter(status='active').select_related('user').prefetch_related('photos')
        self.filterset = CarFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['total_count'] = self.filterset.qs.count()
        if self.request.user.is_authenticated:
            context['favorite_ids'] = set(Favorite.objects.filter(user=self.request.user).values_list('listing_id', flat=True))
        else:
            context['favorite_ids'] = set()
        context['seo_title'] = 'Каталог авто - ALAY AVTO 777'
        context['seo_description'] = 'Каталог автомобилей в Бишкеке. Продажа, рассрочка, Trade-In.'
        return context


class CarDetailView(DetailView):
    model = CarListing
    template_name = 'cars/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        session_key = f'viewed_car_{obj.id}'
        if not self.request.session.get(session_key):
            obj.views_count += 1
            obj.save(update_fields=['views_count'])
            self.request.session[session_key] = True
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.object
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(user=self.request.user, listing=self.object).exists()
        context['similar'] = CarListing.objects.filter(make=self.object.make, status='active').exclude(id=self.object.id)[:4]
        context['seo_title'] = f'{self.object.title} - ALAY AVTO 777'
        context['seo_description'] = self.object.description[:150]
        return context


class AddCarView(LoginRequiredMixin, CreateView):
    model = CarListing
    form_class = CarListingForm
    template_name = 'cars/add.html'
    login_url = '/accounts/login/'

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        if not listing.title:
            listing.title = f"{listing.get_make_display()} {listing.model_name} {listing.year}"
        listing.save()

        if listing.currency == 'usd':
            listing.price_kgs = int(listing.price) * 87
        else:
            listing.price_kgs = listing.price
        listing.save(update_fields=['price_kgs'])

        base = slugify(f"{listing.make}-{listing.model_name}-{listing.year}-{listing.id}")
        listing.slug = base
        listing.save(update_fields=['slug'])

        # Берём ВСЕ файлы из request.FILES.getlist('photos')
        photos = self.request.FILES.getlist('photos')
        for i, photo in enumerate(photos[:10]):
            CarPhoto.objects.create(
                listing=listing,
                image=photo,
                is_main=(i == 0),
                order=i
            )

        messages.success(self.request, 'Объявление успешно опубликовано!')
        return redirect(listing.get_absolute_url())

    def form_invalid(self, form):
        messages.error(self.request, f'Ошибка в форме: {form.errors}')
        return super().form_invalid(form)


class EditCarView(LoginRequiredMixin, UpdateView):
    model = CarListing
    form_class = CarListingForm
    template_name = 'cars/add.html'


class DeleteCarView(LoginRequiredMixin, DeleteView):
    model = CarListing
    success_url = '/profile/'
    template_name = 'cars/delete_confirm.html'


class MarkSoldView(LoginRequiredMixin, View):
    def post(self, request, slug):
        listing = get_object_or_404(CarListing, slug=slug, user=request.user)
        listing.status = 'sold'
        listing.save(update_fields=['status'])
        return redirect('accounts:profile')


class GetModelsView(View):
    def get(self, request):
        make = request.GET.get('make', '')
        return JsonResponse({'models': MODELS_BY_MAKE.get(make, [])})


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request):
        listing_id = request.POST.get('listing_id')
        listing = get_object_or_404(CarListing, id=listing_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
        if not created:
            fav.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})


class IncrementViewView(View):
    def post(self, request):
        listing = get_object_or_404(CarListing, id=request.POST.get('listing_id'))
        listing.views_count += 1
        listing.save(update_fields=['views_count'])
        return JsonResponse({'views': listing.views_count})
