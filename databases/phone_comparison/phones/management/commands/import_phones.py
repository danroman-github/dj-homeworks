# import os
# import sys
# from pathlib import Path

import csv
from django.core.management.base import BaseCommand
from phones.models import Phone


# Принудительно добавляем путь к проекту
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# sys.path.append(str(BASE_DIR))


class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            Phone.objects.create(
                name=phone['name'],
                price=float(phone['price']),
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'].lower() == 'true',
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully imported phone: {phone["name"]}'))

        self.stdout.write(self.style.SUCCESS('All phones imported successfully'))
