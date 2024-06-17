from rest_framework import serializers
from .models import Channel
from django.contrib.auth.models import User


class ChannelSerializer(serializers.ModelSerializer):
    sender_user = serializers.ReadOnlyField(source='sender_user.username')
    recipient_user = serializers.ReadOnlyField(source='recipient_user.username')

    class Meta:
        model = Channel
        fields = '__all__'


class CreateChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'sender_user', 'recipient_user', 'accepted']


class AcceptChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.IntegerField()
    secret_key = serializers.CharField(max_length=64)

    class Meta:
        model = Channel
        fields = ['channel_id', 'secret_key']