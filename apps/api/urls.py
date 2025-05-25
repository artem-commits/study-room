from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, RoomViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
] 