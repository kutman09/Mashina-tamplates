from django import forms
from .models import CarListing


class CarListingForm(forms.ModelForm):
    class Meta:
        model = CarListing
        fields = [
            'make', 'model_name', 'generation', 'year', 'mileage',
            'body_type', 'transmission', 'fuel', 'engine_volume', 'power',
            'drive', 'steering', 'color', 'owners_count', 'condition',
            'price', 'currency', 'is_negotiable', 'has_installment',
            'region', 'city', 'description',
            'is_customs_cleared', 'has_gas_equipment', 'is_urgent',
            'is_exchange_possible',
        ]

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and (year < 1990 or year > 2026):
            raise forms.ValidationError('Укажите год от 1990 до 2026')
        return year

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля')
        return price

    def clean_mileage(self):
        mileage = self.cleaned_data.get('mileage')
        if mileage is not None and mileage < 0:
            raise forms.ValidationError('Пробег не может быть отрицательным')
        return mileage
