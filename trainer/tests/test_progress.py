from django.shortcuts import render, redirect, reverse
from django.test import TestCase, Client
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from trainer.forms import UserRegistrationForm
from trainer.models import Notification, Progress, Client, CustomUser as User
import json
import decimal
from datetime import datetime
from django.http import Http404


class TestProgressViews(TestCase):
    fixtures = ['test_users', 'test_progress', 'test_clients']

    def test_add_new_progress(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.post(reverse('trainer:submit_progress'),
                                    {'weight': 200.0, 'date': '2019-7-1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        progress = Progress.objects.get(id=4).weight
        self.assertEqual(progress, 200)
        weight = response.context['client'].weight
        self.assertEqual(200, weight)

    def test_get_progress(self):
        user = User.objects.get(id=2)
        self.client.force_login(user)
        response = self.client.get(reverse('trainer:get_progress', kwargs={'pk': user.pk}))
        progress = json.loads(response.content)
        weight = decimal.Decimal(progress[0]['weight'])
        self.assertEqual(weight, 220.0)

    def test_get_all_clients(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get(reverse('trainer:get_clients'))
        clients = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
