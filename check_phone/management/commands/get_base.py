import csv, io
import requests
from django.core.management.base import BaseCommand
from check_phone import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        settings, created = models.Settings.objects.get_or_create()
        if created or not settings.urls:
            settings.urls = ['https://rossvyaz.ru/data/ABC-3xx.csv',
                             'https://rossvyaz.ru/data/ABC-4xx.csv',
                             'https://rossvyaz.ru/data/ABC-8xx.csv',
                             'https://rossvyaz.ru/data/DEF-9xx.csv']
        new = []
        ok = True
        for url in settings.urls:
            response = requests.get(url)
            # TODO Проверка на совпадение crc с предыдущей версией, т.к. заявленное обновление базы только раз в месяц
            try:
                reestr = csv.reader(io.StringIO(response.content.decode('utf-8')), delimiter=';')
                for row in reestr:
                    obj = models.Phones(
                        code=row[0], start=row[1], finish=row[2], numbers=row[3], operator=row[4], location=row[5])
                    new.append(obj)
            except:
                ok = False
                break
        if ok:
            settings.base_ready = False
            settings.save()
            models.Phones.objects.all().delete()
            models.Phones.objects.bulk_create(new, 16535)
            settings.base_ready = True
            settings.save()
