import os

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from security.models import Channel
from security.serializers import ChannelSerializer, AcceptChannelSerializer

Base = 2
Modulus = int('A4E02E7144D7189965AA9901013921BD721AE84072B4F41A3ED4AD3F5DC1C403', 16)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Channel.objects.filter(sender_user=user) | Channel.objects.filter(recipient_user=user)

    def perform_create(self, serializer):
        name = os.urandom(5).hex()
        serializer.save(sender_user=self.request.user, name=name)

    @action(detail=False, methods=['post'])
    def accept_channel(self, request):
        serializer = AcceptChannelSerializer(data=request.data)
        if serializer.is_valid():
            channel_id = serializer.validated_data['channel_id']
            secret_key = int(serializer.validated_data['secret_key'], 16)
            channel = Channel.objects.get(pk=channel_id)
            if request.user == channel.recipient_user:
                channel.initial_recipient_secret = pow(Base, secret_key, Modulus)
                channel.accepted = True
                channel.save()
                return Response({'recipient_secret': channel.initial_recipient_secret}, status=status.HTTP_200_OK)
            elif request.user == channel.sender_user:
                channel.initial_sender_secret = pow(Base, secret_key, Modulus)
                channel.accepted = True
                channel.save()
                return Response({'recipient_secret': channel.initial_sender_secret}, status=status.HTTP_200_OK)
            return Response({'error': 'User not authorized on this channel'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeyGenerationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        channel_id = request.data.get('channel_id')
        secret_key = int(request.data.get('secret_key'), 16)
        channel = Channel.objects.get(pk=channel_id)
        if request.user == channel.sender_user and channel.accepted:
            key = pow(channel.initial_recipient_secret, secret_key, Modulus)
            return Response({'key': key}, status=status.HTTP_200_OK)
        elif request.user == channel.recipient_user and channel.accepted:
            key = pow(channel.initial_sender_secret, secret_key, Modulus)
            return Response({'key': key}, status=status.HTTP_200_OK)
        return Response({'error': 'Unauthorized or channel not accepted'}, status=status.HTTP_403_FORBIDDEN)

