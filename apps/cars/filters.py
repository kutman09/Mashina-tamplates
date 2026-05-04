import django_filters
from .models import (
    BODY_TYPE_CHOICES,
    DRIVE_CHOICES,
    FUEL_CHOICES,
    MAKE_CHOICES,
    REGION_CHOICES,
    TRANSMISSION_CHOICES,
    CarListing,
)


class CarFilter(django_filters.FilterSet):
    make = django_filters.ChoiceFilter(choices=MAKE_CHOICES, label='Марка')
    model_name = django_filters.CharFilter(lookup_expr='icontains', label='Модель')
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte', label='Год от')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte', label='Год до')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    region = django_filters.ChoiceFilter(choices=REGION_CHOICES, label='Регион')
    body_type = django_filters.ChoiceFilter(choices=BODY_TYPE_CHOICES, label='Тип кузова')
    transmission = django_filters.ChoiceFilter(choices=TRANSMISSION_CHOICES, label='КПП')
    fuel = django_filters.ChoiceFilter(choices=FUEL_CHOICES, label='Топливо')
    drive = django_filters.ChoiceFilter(choices=DRIVE_CHOICES, label='Привод')
    mileage_min = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte', label='Пробег от')
    mileage_max = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte', label='Пробег до')
    engine_min = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='gte', label='Объем от')
    engine_max = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='lte', label='Объем до')
    has_photo = django_filters.BooleanFilter(label='С фото')
    has_installment = django_filters.BooleanFilter(label='Рассрочка')
    is_urgent = django_filters.BooleanFilter(label='Срочно')
    is_customs_cleared = django_filters.BooleanFilter(label='Растаможен')
    has_gas_equipment = django_filters.BooleanFilter(label='Газовое оборудование')
    ordering = django_filters.OrderingFilter(
        choices=[
            ('-created_at', 'Сначала новые'),
            ('created_at', 'Сначала старые'),
            ('price', 'Цена: по возрастанию'),
            ('-price', 'Цена: по убыванию'),
            ('year', 'Год: старые'),
            ('-year', 'Год: новые'),
            ('mileage', 'Пробег: меньше'),
        ]
    )

    class Meta:
        model = CarListing
        fields = []
