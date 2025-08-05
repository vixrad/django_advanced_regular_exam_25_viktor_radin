from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.models import User

class AccountTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name="Full Admin")
        Group.objects.get_or_create(name="Staff Admin")

    def test_register_customer(self):
        response = self.client.post(reverse('register'), {
            'email': 'customer@test.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'is_owner': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='customer@test.com').exists())

    def test_register_owner_assigns_group(self):
        response = self.client.post(reverse('register'), {
            'email': 'owner@test.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'is_owner': True,
            'company_number': '123456'
        })
        user = User.objects.get(email='owner@test.com')
        self.assertTrue(user.groups.filter(name="Full Admin").exists())

    def test_login_valid_credentials(self):
        user = User.objects.create_user(email='login@test.com', password='Pass1234')
        response = self.client.post(reverse('login'), {'username': 'login@test.com', 'password': 'Pass1234'})
        self.assertEqual(response.status_code, 302)