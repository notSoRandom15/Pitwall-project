from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from security.models import Channel
from security.serializers import ChannelSerializer, AcceptChannelSerializer


# Create your views here.

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def get_queryset(self):
        user = self.request.user
        return Channel.objects.filter(sender_user=user) | Channel.objects.filter(recipient_user=user)

    def perform_create(self, serializer):
        serializer.save(sender_user=self.request.user)

    @action(detail=False, methods=['post'])
    def accept_channel(self, request):
        serializer = AcceptChannelSerializer(data=request.data)
        if serializer.is_valid():
            channel_id = serializer.validated_data['channel_id']
            secret_key = int(serializer.validated_data['secret_key'], 16)
            channel = Channel.objects.get(pk=channel_id)
            if request.user == channel.recipient_user:
                modulus = 2 ** 256 - 189
                base = 5
                channel.initial_recipient_secret = pow(base, secret_key, modulus)
                channel.accepted = True
                channel.save()
                return Response({'recipient_secret': channel.initial_recipient_secret}, status=status.HTTP_200_OK)
            elif request.user == channel.sender_user:
                modulus = 2 ** 256 - 189
                base = 5
                channel.initial_sender_secret = pow(base, secret_key, modulus)
                channel.accepted = True
                channel.save()
                return Response({'recipient_secret': channel.initial_sender_secret}, status=status.HTTP_200_OK)
            return Response({'error': 'User not authorized on this channel'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)