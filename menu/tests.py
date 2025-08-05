from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from restaurants.models import Restaurant
from menu.models import MenuCategory

class MenuTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="owner@test.com", password="Pass1234", is_owner=True)
        self.client.login(username="owner@test.com", password="Pass1234")
        self.restaurant = Restaurant.objects.create(owner=self.owner, name="R1", city="C", postal_code="123", street_name="S", street_number="1", phone="123")

    def test_add_category(self):
        response = self.client.post(reverse('add_category', args=[self.restaurant.id]), {
            'name': 'Starters'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MenuCategory.objects.filter(name='Starters').exists())