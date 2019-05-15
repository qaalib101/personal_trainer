from django.shortcuts import render, redirect, reverse
from django.test import TestCase, Client
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from trainer.forms import UserRegistrationForm
from trainer.models import Progress, Client, CustomUser as User
from PIL import Image
import os


class TestClientViews(TestCase):
    def test_client_registration_get(self):
        response = self.client.get(reverse('trainer:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_post(self):
        response = self.client.post(reverse('trainer:register'),
                                    {'username':'qaalib101', 'first_name':'qaalib', 'last_name':'farah',
                                     'password1':'asdfghj123', 'password2':'asdfghj123', 'email':'qaalibomer@gmail.com'}
                                    ,follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'users/setup_client.html')


class TestSetupClient(TestCase):
    fixtures = ['test_users', 'test_clients']

    def test_new_client(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.post(reverse('trainer:edit_profile'), {'birthday':'1998-01-05', 'weight': 240.9}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_incorrect_form(self):
        user = User.objects.get(pk=3)
        self.client.force_login(user)
        response = self.client.post(reverse('trainer:edit_profile'), {'bmi': '24.5'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/setup_client.html')
        self.assertContains(response, 'Form is not valid')

    def test_user_profile_page(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(reverse('trainer:user_profile', kwargs={'user_pk': user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, f"{user.username}'s profile page")

    def test_user_profile_not_user_page(self):
        user = User.objects.get(pk=1)
        expected = User.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(reverse('trainer:user_profile', kwargs={'user_pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, f"{expected.username}'s profile page")

    def test_user_profile_with_no_client(self):
        user = User.objects.get(pk=4)
        self.client.force_login(user)
        response = self.client.get(reverse('trainer:user_profile', kwargs={'user_pk': user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/setup_client.html')
        self.assertContains(response, 'Set up client')

    def test_set_up_client(self):
        user = User.objects.get(pk=3)
        self.client.force_login(user)
        with Image.open('trainer/media/test/download.jpg') as img:
            response = self.client.post(reverse('trainer:edit_profile'),
                                        {'birthday': '1998-01-05', 'photo': img, 'weight': 240.5},
                                        follow=True)
            self.assertEqual(response.status_code, 200)
