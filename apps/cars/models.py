from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify

MAKE_CHOICES = [
    ('toyota', 'Toyota'),
    ('bmw', 'BMW'),
    ('mercedes', 'Mercedes-Benz'),
    ('audi', 'Audi'),
    ('hyundai', 'Hyundai'),
    ('kia', 'Kia'),
    ('chevrolet', 'Chevrolet'),
    ('lexus', 'Lexus'),
    ('nissan', 'Nissan'),
    ('honda', 'Honda'),
    ('mazda', 'Mazda'),
    ('mitsubishi', 'Mitsubishi'),
    ('subaru', 'Subaru'),
    ('volkswagen', 'Volkswagen'),
    ('ford', 'Ford'),
    ('porsche', 'Porsche'),
    ('land_rover', 'Land Rover'),
    ('genesis', 'Genesis'),
    ('haval', 'Haval'),
    ('other', 'Другое'),
]

MODELS_BY_MAKE = {
    'toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser', 'Highlander'],
    'bmw': ['3 Series', '5 Series', 'X3', 'X5'],
    'mercedes': ['E-Class', 'GLE', 'G-Class'],
    'audi': ['A6', 'Q7'],
    'hyundai': ['Santa Fe', 'Sonata'],
    'kia': ['Sportage', 'Sorento', 'K5'],
    'chevrolet': ['Tahoe'],
    'lexus': ['RX', 'LX', 'ES'],
    'nissan': ['Patrol', 'X-Trail'],
    'honda': ['CR-V'],
    'mazda': ['CX-5'],
    'mitsubishi': ['Pajero Sport'],
    'subaru': ['Forester'],
    'volkswagen': ['Tiguan'],
    'ford': ['Explorer'],
    'land_rover': ['Defender'],
    'porsche': ['Cayenne'],
    'genesis': ['GV80'],
    'haval': ['H9'],
    'other': ['Другая модель'],
}

REGION_CHOICES = [
    ('bishkek', 'Бишкек'),
    ('osh', 'Ош'),
    ('chuy', 'Чуй областы'),
    ('issyk_kul', 'Ысык-Куль областы'),
    ('jalal_abad', 'Жалал-Абад областы'),
    ('batken', 'Баткен областы'),
    ('naryn', 'Нарын областы'),
    ('talas', 'Талас областы'),
    ('osh_region', 'Ош областы'),
]
BODY_TYPE_CHOICES = [
    ('sedan', 'Седан'),
    ('suv', 'Внедорожник / SUV'),
    ('hatchback', 'Хэтчбек'),
    ('wagon', 'Универсал'),
    ('coupe', 'Купе'),
    ('convertible', 'Кабриолет'),
    ('minivan', 'Минивэн'),
    ('pickup', 'Пикап'),
    ('crossover', 'Кроссовер'),
    ('truck', 'Грузовик'),
    ('van', 'Фургон'),
    ('other', 'Другой'),
]
TRANSMISSION_CHOICES = [
    ('automatic', 'Автомат'),
    ('manual', 'Механика'),
    ('robot', 'Робот'),
    ('variator', 'Вариатор'),
]
FUEL_CHOICES = [
    ('petrol', 'Бензин'),
    ('diesel', 'Дизель'),
    ('gas', 'Газ (LPG)'),
    ('hybrid', 'Гибрид'),
    ('electric', 'Электро'),
    ('gas_petrol', 'Газ/Бензин'),
]
DRIVE_CHOICES = [
    ('fwd', 'Передний'),
    ('rwd', 'Задний'),
    ('awd', 'Полный (AWD/4WD)'),
]
STEERING_CHOICES = [
    ('left', 'Левый руль'),
    ('right', 'Правый руль'),
]
CONDITION_CHOICES = [
    ('used', 'Б/У'),
    ('new', 'Новый'),
    ('damaged', 'Аварийный'),
]
CURRENCY_CHOICES = [('usd', 'USD ($)'), ('kgs', 'Сом (с)')]
STATUS_CHOICES = [('active', 'Активно'), ('sold', 'Продано'), ('hidden', 'Скрыто')]
COLOR_CHOICES = [('white', 'Белый'), ('black', 'Черный'), ('silver', 'Серебристый'), ('red', 'Красный'), ('other', 'Другой')]


class CarListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=350)
    make = models.CharField(max_length=50, choices=MAKE_CHOICES)
    model_name = models.CharField(max_length=100)
    generation = models.CharField(max_length=100, blank=True)
    year = models.IntegerField()
    mileage = models.IntegerField()
    body_type = models.CharField(max_length=30, choices=BODY_TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    engine_volume = models.DecimalField(max_digits=4, decimal_places=1)
    drive = models.CharField(max_length=10, choices=DRIVE_CHOICES)
    steering = models.CharField(max_length=10, choices=STEERING_CHOICES, default='left')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True)
    power = models.IntegerField(null=True, blank=True)
    owners_count = models.IntegerField(default=1)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    price = models.DecimalField(max_digits=12, decimal_places=0)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='usd')
    price_kgs = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    is_negotiable = models.BooleanField(default=False)
    has_installment = models.BooleanField(default=False)
    region = models.CharField(max_length=30, choices=REGION_CHOICES)
    city = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    has_photo = models.BooleanField(default=True)
    is_customs_cleared = models.BooleanField(default=False)
    has_gas_equipment = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    is_exchange_possible = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.get_make_display()} {self.model_name} {self.year}'
        super().save(*args, **kwargs)
        expected_slug = slugify(f'{self.make}-{self.model_name}-{self.year}-{self.id}')
        if self.slug != expected_slug:
            self.slug = expected_slug
            CarListing.objects.filter(pk=self.pk).update(slug=expected_slug)
        if self.currency == 'usd' and self.price:
            self.price_kgs = int(self.price) * 87
            CarListing.objects.filter(pk=self.pk).update(price_kgs=self.price_kgs)

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'slug': self.slug})

    def get_main_photo(self):
        return self.photos.filter(is_main=True).first() or self.photos.first()


class CarPhoto(models.Model):
    listing = models.ForeignKey(CarListing, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='cars/photos/%Y/%m/')
    is_main = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_main', 'order']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(CarListing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    region = models.CharField(max_length=30, choices=REGION_CHOICES, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Профиль: {self.user.username}'
