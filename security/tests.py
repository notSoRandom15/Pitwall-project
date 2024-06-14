from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from security.models import Channel


class ChannelTests(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.recipient = User.objects.create_user(username='recipient', password='password')
        self.sender_token = RefreshToken.for_user(self.sender).access_token
        self.recipient_token = RefreshToken.for_user(self.recipient).access_token

    def create_channel_test(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.sender_token}')
        response = self.client.post('api/channels/', {'recipient_user': self.recipient.id})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)

    def accept_channel_test(self):
        channel = Channel.objects.create(sender_user=self.sender, recipient_user=self.recipient, name='test')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.recipient_token}')
        response = self.client.post('/api/channels/accept_channel', {
            'channel_id': channel.id, 'secret_key': '1234567890abcdef',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('recipient_secret', response.data)

    def generate_key_test(self):
        channel = Channel.objects.create(sender_user=self.sender, recipient_user=self.recipient, name='test', accepted=True, initial_sender_secret=1234)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.sender_token}')
        response = self.client.post('/api/generate-key/', {'channel_id': channel.id, 'secret_key': '1234567890abcdef'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('key', response.data)
