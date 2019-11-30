from django.test import TestCase, Client
from django.urls import reverse

from check_phone import models


class AllTestClass(TestCase):

    def setUp(self):
        models.Settings.objects.all().delete()

    def test_wrongnumber(self):
        body = '7123'
        response = Client().post(reverse('api'), body, content_type="application/json")
        self.assertEqual(response.json().get('code'), 2)


    def test_technicalwork(self):
        body = '79833839583'
        response = Client().post(reverse('api'), body, content_type="application/json")
        self.assertEqual(response.json().get('code'), 3)
