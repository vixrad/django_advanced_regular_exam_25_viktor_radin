from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from restaurants.models import Restaurant

class RestaurantTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="owner@test.com", password="Pass1234", is_owner=True)
        self.client.login(username="owner@test.com", password="Pass1234")

    def test_add_restaurant(self):
        response = self.client.post(reverse('add_restaurant'), {
            'name': 'My Test Restaurant',
            'description': 'Test description',
            'city': 'London',
            'postal_code': 'E1 6AN',
            'street_name': 'Baker St',
            'street_number': '221B',
            'phone': '+441234567890'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Restaurant.objects.filter(name='My Test Restaurant').exists())