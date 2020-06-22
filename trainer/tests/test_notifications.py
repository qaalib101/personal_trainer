from django.shortcuts import reverse
from django.test import TestCase
from trainer.submodels.train_models import Notification, CustomUser as User
from trainer.views_client import save_notification
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
