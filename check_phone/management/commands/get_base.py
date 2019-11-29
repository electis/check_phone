import csv, io
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from check_phone import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        settings, created = models.Settings.objects.get_or_create()
        # if created or not settings.urls:
        #     settings.urls = ['https://rossvyaz.ru/data/ABC-3xx.csv',
        urls = ['https://rossvyaz.ru/data/ABC-3xx.csv',
                'https://rossvyaz.ru/data/ABC-4xx.csv',
                'https://rossvyaz.ru/data/ABC-8xx.csv',
                'https://rossvyaz.ru/data/DEF-9xx.csv']
        # for url in settings.urls:
        with transaction.atomic():
            models.Phones.objects.all().delete()
            for url in urls:
                print('Get data from', url)
                response = requests.get(url)
                new = []
                # TODO Проверка на совпадение crc с предыдущей версией, т.к. заявленное обновление базы только раз в месяц
                try:
                    reestr = csv.reader(io.StringIO(response.content.decode('utf-8')), delimiter=';')
                    for row in reestr:

                        if row[0].isdigit() and row[1].isdigit() and row[2].isdigit() and row[3].isdigit() \
                                and len(row[0]) == 3 and len(row[1]) == 7 and len(row[2]) == 7:
                            operator, created = models.Operator.objects.get_or_create(operator=row[4])
                            location, created = models.Location.objects.get_or_create(location=row[5])
                            obj = models.Phones(code=row[0], start=row[1], finish=row[2], numbers=row[3],
                                                operator=operator, location=location)
                            new.append(obj)
                        else:
                            raise Exception('CSV data error')
                    settings.base_ready = False
                    settings.save()
                    print('Fill DB with data')
                    models.Phones.objects.bulk_create(new)
                    settings.base_ready = True
                    settings.save()
                except Exception as e:
                    print(e)
                    transaction.rollback()
                    break
            print('All OK')
