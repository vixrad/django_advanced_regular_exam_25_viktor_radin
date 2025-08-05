from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from restaurants.models import Restaurant
from reservations.models import Reservation
from datetime import datetime, timedelta

class ReservationTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(email="cust@test.com", password="Pass1234")
        self.owner = User.objects.create_user(email="owner@test.com", password="Pass1234", is_owner=True)
        self.restaurant = Restaurant.objects.create(owner=self.owner, name="R1", city="C", postal_code="123", street_name="S", street_number="1", phone="123")
        self.client.login(username="cust@test.com", password="Pass1234")

    def test_create_reservation(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        response = self.client.post(reverse('reservation_create_with_restaurant', args=[self.restaurant.id]), {
            'reservation_time': future_date,
            'number_of_people': 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reservation.objects.exists())

    def test_owner_cannot_book(self):
        self.client.logout()
        self.client.login(username="owner@test.com", password="Pass1234")
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        response = self.client.post(reverse('reservation_create_with_restaurant', args=[self.restaurant.id]), {
            'reservation_time': future_date,
            'number_of_people': 2
        })
        self.assertEqual(response.status_code, 302)  # redirected
        self.assertFalse(Reservation.objects.exists())