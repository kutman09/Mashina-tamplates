from django.contrib import admin
from .models import CarListing, CarPhoto, Favorite, UserProfile


class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 3


@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'make', 'model_name', 'year', 'price', 'region', 'status', 'is_featured', 'views_count', 'created_at']
    list_filter = ['make', 'status', 'is_featured', 'has_installment', 'region', 'fuel', 'body_type']
    search_fields = ['title', 'model_name', 'user__username']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'slug']
    inlines = [CarPhotoInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'region']
