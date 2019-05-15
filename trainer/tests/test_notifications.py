from django.shortcuts import render, redirect, reverse
from django.test import TestCase, Client
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from trainer.forms import UserRegistrationForm
from trainer.models import Notification, Progress, Client, CustomUser as User
from trainer.views_client import save_notification
from django.http import Http404
from datetime import datetime


class TestNotificationView(TestCase):
    fixtures = ['test_users', 'test_clients']

    def test_saving_notification(self):
        user = User.objects.get(pk=1)
        client = User.objects.get(pk=2)
        self.client.force_login(user)
        notification = save_notification(client, datetime.now(), 'Example notification')
        expected = Notification.objects.get(user=client)
        self.assertEqual(expected, notification)

    def test_notification(self):
        trainer = User.objects.get(pk=1)
        client = User.objects.get(pk=2)
        self.client.force_login(trainer)
        notification = save_notification(client, datetime.now(), 'Example notification')
        expected = Notification.objects.get(user=client)
        self.assertEqual(expected, notification)
        response = self.client.get(reverse('trainer:user_profile', kwargs={'user_pk': 1}))
        self.assertTemplateUsed(response, 'users/trainer.html')
        template = response.context['notifications'][0]
        self.assertEqual(template, expected)
