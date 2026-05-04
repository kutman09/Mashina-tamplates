from pathlib import Path
import random
import urllib.request
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.cars.models import CarListing, CarPhoto, UserProfile

PHOTO_URLS = [
    'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800',
    'https://images.unsplash.com/photo-1559416523-140ddc3d238c?w=800',
    'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800',
    'https://images.unsplash.com/photo-1520031441872-265e4ff70366?w=800',
    'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800',
    'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800',
    'https://images.unsplash.com/photo-1493238792000-8113da705763?w=800',
    'https://images.unsplash.com/photo-1629897048514-3dd7414fe72a?w=800',
    'https://images.unsplash.com/photo-1617469767-16af3e8edaad?w=800',
    'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800',
]

SAMPLE_CARS = [
    ('toyota', 'Camry', 2021, 35000, 'sedan', 'automatic', 'petrol', 2.5, 'fwd', 'left', 28000, 'bishkek', 'used'),
    ('toyota', 'Land Cruiser', 2020, 55000, 'suv', 'automatic', 'petrol', 4.0, 'awd', 'left', 75000, 'bishkek', 'used'),
    ('toyota', 'RAV4', 2022, 18000, 'suv', 'automatic', 'hybrid', 2.5, 'awd', 'left', 35000, 'bishkek', 'used'),
    ('toyota', 'Highlander', 2019, 72000, 'suv', 'automatic', 'petrol', 3.5, 'awd', 'left', 42000, 'osh', 'used'),
    ('bmw', 'X5', 2021, 28000, 'suv', 'automatic', 'petrol', 3.0, 'awd', 'left', 82000, 'bishkek', 'used'),
    ('bmw', '5 Series', 2020, 45000, 'sedan', 'automatic', 'petrol', 2.0, 'rwd', 'left', 48000, 'bishkek', 'used'),
    ('bmw', 'X3', 2022, 15000, 'suv', 'automatic', 'petrol', 2.0, 'awd', 'left', 58000, 'bishkek', 'used'),
    ('mercedes', 'E-Class', 2021, 32000, 'sedan', 'automatic', 'petrol', 2.0, 'rwd', 'left', 55000, 'bishkek', 'used'),
    ('mercedes', 'GLE', 2020, 48000, 'suv', 'automatic', 'diesel', 3.0, 'awd', 'left', 68000, 'chuy', 'used'),
    ('mercedes', 'G-Class', 2019, 62000, 'suv', 'automatic', 'petrol', 4.0, 'awd', 'left', 110000, 'bishkek', 'used'),
    ('lexus', 'RX', 2022, 12000, 'crossover', 'automatic', 'hybrid', 2.5, 'awd', 'left', 52000, 'bishkek', 'used'),
    ('lexus', 'LX', 2021, 35000, 'suv', 'automatic', 'petrol', 5.7, 'awd', 'left', 95000, 'bishkek', 'used'),
    ('lexus', 'ES', 2021, 28000, 'sedan', 'automatic', 'hybrid', 2.5, 'fwd', 'left', 45000, 'osh', 'used'),
    ('hyundai', 'Santa Fe', 2021, 42000, 'suv', 'automatic', 'petrol', 2.5, 'awd', 'left', 30000, 'chuy', 'used'),
    ('hyundai', 'Sonata', 2022, 22000, 'sedan', 'automatic', 'petrol', 2.5, 'fwd', 'left', 24000, 'bishkek', 'used'),
    ('kia', 'Sportage', 2022, 19000, 'crossover', 'automatic', 'petrol', 2.0, 'awd', 'left', 26000, 'bishkek', 'used'),
    ('kia', 'Sorento', 2021, 35000, 'suv', 'automatic', 'diesel', 2.2, 'awd', 'left', 32000, 'issyk_kul', 'used'),
    ('audi', 'Q7', 2020, 58000, 'suv', 'automatic', 'diesel', 3.0, 'awd', 'left', 58000, 'bishkek', 'used'),
    ('audi', 'A6', 2021, 38000, 'sedan', 'automatic', 'petrol', 2.0, 'awd', 'left', 45000, 'bishkek', 'used'),
    ('chevrolet', 'Tahoe', 2022, 25000, 'suv', 'automatic', 'petrol', 5.3, 'awd', 'left', 62000, 'bishkek', 'used'),
    ('nissan', 'Patrol', 2020, 55000, 'suv', 'automatic', 'petrol', 5.6, 'awd', 'left', 58000, 'chuy', 'used'),
    ('nissan', 'X-Trail', 2021, 38000, 'suv', 'variator', 'petrol', 2.0, 'awd', 'left', 28000, 'osh', 'used'),
    ('honda', 'CR-V', 2022, 18000, 'crossover', 'automatic', 'petrol', 1.5, 'awd', 'left', 30000, 'bishkek', 'used'),
    ('subaru', 'Forester', 2021, 42000, 'crossover', 'variator', 'petrol', 2.5, 'awd', 'left', 25000, 'bishkek', 'used'),
    ('mazda', 'CX-5', 2022, 16000, 'crossover', 'automatic', 'petrol', 2.5, 'awd', 'left', 32000, 'chuy', 'used'),
    ('toyota', 'Camry', 2019, 85000, 'sedan', 'automatic', 'gas_petrol', 2.5, 'fwd', 'left', 18000, 'jalal_abad', 'used'),
    ('toyota', 'Corolla', 2020, 62000, 'sedan', 'manual', 'petrol', 1.6, 'fwd', 'left', 14000, 'batken', 'used'),
    ('volkswagen', 'Tiguan', 2021, 35000, 'crossover', 'robot', 'petrol', 1.4, 'awd', 'left', 28000, 'bishkek', 'used'),
    ('ford', 'Explorer', 2020, 48000, 'suv', 'automatic', 'petrol', 3.5, 'awd', 'left', 38000, 'bishkek', 'used'),
    ('land_rover', 'Defender', 2022, 22000, 'suv', 'automatic', 'petrol', 3.0, 'awd', 'left', 85000, 'bishkek', 'used'),
    ('porsche', 'Cayenne', 2020, 45000, 'suv', 'automatic', 'petrol', 3.0, 'awd', 'left', 72000, 'bishkek', 'used'),
    ('mitsubishi', 'Pajero Sport', 2021, 38000, 'suv', 'automatic', 'diesel', 2.4, 'awd', 'left', 32000, 'naryn', 'used'),
    ('kia', 'K5', 2022, 15000, 'sedan', 'automatic', 'petrol', 1.6, 'fwd', 'left', 22000, 'talas', 'used'),
    ('genesis', 'GV80', 2022, 18000, 'suv', 'automatic', 'petrol', 2.5, 'awd', 'left', 55000, 'bishkek', 'used'),
    ('haval', 'H9', 2023, 8000, 'suv', 'automatic', 'petrol', 2.0, 'awd', 'left', 35000, 'osh_region', 'used'),
]


class Command(BaseCommand):
    help = 'Populate demo car listings'

    def handle(self, *args, **options):
        seller, _ = User.objects.get_or_create(username='seller')
        seller.set_password('test12345')
        seller.save()
        UserProfile.objects.get_or_create(user=seller, defaults={'phone': '+996500070809'})

        CarPhoto.objects.all().delete()
        CarListing.objects.all().delete()

        target_dir = Path(settings.MEDIA_ROOT) / 'cars' / 'photos' / 'seed'
        target_dir.mkdir(parents=True, exist_ok=True)

        downloaded = []
        for idx, url in enumerate(PHOTO_URLS):
            file_path = target_dir / f'car_{idx}.jpg'
            try:
                urllib.request.urlretrieve(url, file_path)
                downloaded.append(file_path)
            except Exception:
                continue
        if not downloaded:
            fallback = settings.BASE_DIR / 'static' / 'images' / 'hero-bg.jpg'
            downloaded.append(fallback)

        installment_ids = set(random.sample(range(len(SAMPLE_CARS)), 11))
        for idx, row in enumerate(SAMPLE_CARS):
            make, model, year, mileage, body, transmission, fuel, engine, drive, steering, price, region, condition = row
            description = (
                f"{make.title()} {model} {year} года в хорошем состоянии. Автомобиль обслужен, "
                f"двигатель {engine} л работает ровно, коробка {transmission}. Подвеска без посторонних звуков, "
                f"салон аккуратный, пробег {mileage} км подтверждается. Машина привезена из Кореи, документы в порядке, "
                f"возможна проверка на СТО и разумный торг у капота."
            )
            listing = CarListing.objects.create(
                user=seller,
                make=make,
                model_name=model,
                year=year,
                mileage=mileage,
                body_type=body,
                transmission=transmission,
                fuel=fuel,
                engine_volume=engine,
                drive=drive,
                steering=steering,
                price=price,
                region=region,
                condition=condition,
                description=description[:390],
                has_installment=idx in installment_ids,
                is_featured=idx < 6,
                is_customs_cleared=True,
            )
            image_path = downloaded[idx % len(downloaded)]
            with image_path.open('rb') as image_file:
                CarPhoto.objects.create(listing=listing, image=File(image_file, name=image_path.name), is_main=True)

        self.stdout.write(self.style.SUCCESS(f'Created {CarListing.objects.count()} listings'))
