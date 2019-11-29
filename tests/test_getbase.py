from django.test import TestCase
from check_phone import models
from check_phone.management.commands import get_base


class AllTestClass(TestCase):

    def setUp(self):
        models.Settings.objects.all().delete()

    def test_request_error(self):
        settings = models.Settings.objects.create(urls=['tests'])
        get_base.Command().handle()

    def test_normal(self):
        get_base.Command().handle()
