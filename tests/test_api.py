from django.test import TestCase, Client
from django.urls import reverse

from check_phone import models


class AllTestClass(TestCase):

    def setUp(self):
        models.Settings.objects.all().delete()

    def test_all(self):
        body = '79833839583'
        response = Client().post(reverse('api'), body, content_type="application/json")
        self.assertEqual(response.json().get('code'), 3)
