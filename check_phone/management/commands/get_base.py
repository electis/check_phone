import csv, io
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from check_phone import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        settings, created = models.Settings.objects.get_or_create()
        if created or not settings.urls:
            settings.urls = ['https://rossvyaz.ru/data/ABC-3xx.csv',
                             'https://rossvyaz.ru/data/ABC-4xx.csv',
                             'https://rossvyaz.ru/data/ABC-8xx.csv',
                             'https://rossvyaz.ru/data/DEF-9xx.csv']
        settings.base_ready = False
        settings.save()
        with transaction.atomic():
            models.Phones.objects.all().delete()
            for url in settings.urls:
                print('Get data from', url)
                try:
                    response = requests.get(url)
                except:
                    print('Error request')
                    break
                new = []
                # TODO Проверка на совпадение crc с предыдущей версией
                try:
                    reestr = csv.reader(io.StringIO(response.content.decode('utf-8')), delimiter=';')
                    operator_old = location_old = None
                    print('Parse data...')
                    for row in reestr:
                        if row[0].isdigit() and row[1].isdigit() and row[2].isdigit() and row[3].isdigit() \
                                and len(row[0]) == 3 and len(row[1]) == 7 and len(row[2]) == 7:
                            if row[4] != operator_old:
                                operator, created = models.Operator.objects.get_or_create(operator=row[4])
                                operator_old = row[4]
                            if row[5] != location_old:
                                location, created = models.Location.objects.get_or_create(location=row[5])
                                location_old = row[5]
                            obj = models.Phones(code=row[0], start=row[1], finish=row[2], numbers=row[3],
                                                operator=operator, location=location)
                            new.append(obj)
                        else:
                            raise Exception('CSV data error')
                        if len(new) > 65535:
                            print('Fill DB with part of data...')
                            models.Phones.objects.bulk_create(new)
                            new = []
                            print('Continue parse data...')
                    if new:
                        print('Fill DB with part of data...')
                        models.Phones.objects.bulk_create(new)
                except Exception as e:
                    print(e)
                    transaction.rollback()
                    break
        settings.base_ready = True
        settings.save()
        print('All OK')
        return 1
