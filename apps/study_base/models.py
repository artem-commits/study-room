from django.contrib.auth import get_user_model
from django.db import models
from apps.common.models import BaseModel, IsDeletedModel
from django.contrib.auth.models import User


class Topic(IsDeletedModel):
    """
    Represents a topic or category for study rooms.

    This model stores the name of topics that can be associated with study rooms.
    It inherits from IsDeletedModel to support soft deletion functionality.

    Attributes:
        name (str): The name of the topic, maximum length of 200 characters.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Room(IsDeletedModel):
    """
    Represents a study room where users can interact and share messages.

    This model manages study rooms with their associated host, topic, and participants.
    It inherits from IsDeletedModel to support soft deletion functionality.

    Attributes:
        host (User): The user who created and manages the room.
        topic (Topic): The topic associated with the room.
        name (str): The name of the room, maximum length of 200 characters.
        description (str, optional): A detailed description of the room.
        participants (ManyToManyField): Users who have joined the room.
    """

    host = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(get_user_model(), related_name='participants', blank=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.name)


class Message(BaseModel):
    """
    Represents a message posted in a study room.

    This model stores messages sent by users in study rooms.
    It inherits from BaseModel to include common fields like created_at and updated_at.

    Attributes:
        user (User): The user who sent the message.
        room (Room): The room where the message was posted.
        body (str): The content of the message.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.body[0:25]
