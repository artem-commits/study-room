from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.study_base.models import Room, Topic, Message
from .serializers import RoomSerializer, TopicSerializer, MessageSerializer
from drf_spectacular.utils import extend_schema


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing topics
    """
    queryset = Topic.objects.filter(is_deleted=False)
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="List all topics",
        responses={200: TopicSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing study rooms
    """
    queryset = Room.objects.filter(is_deleted=False)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room = self.get_object()
        room.participants.add(request.user)
        return Response({'status': 'joined room'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        room = self.get_object()
        room.participants.remove(request.user)
        return Response({'status': 'left room'})

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing messages in rooms
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get('room_pk')
        if room_id:
            return Message.objects.filter(room_id=room_id)
        return Message.objects.none()

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_pk')
        room = get_object_or_404(Room, id=room_id)
        serializer.save(user=self.request.user, room=room)
