from rest_framework import serializers
from apps.study_base.models import Room, Topic, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'created_at', 'updated_at', 'is_deleted')
        read_only_fields = ('id', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'user', 'room', 'body', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class RoomSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'host', 'topic', 'name', 'description',
                  'participants', 'messages', 'created_at', 'updated_at', 'is_deleted')
        read_only_fields = ('id', 'created_at', 'updated_at')
