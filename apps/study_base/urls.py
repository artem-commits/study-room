from django.urls import path
from .views import (
    HomeListView,
    RoomCreateView,
    RoomDetailView,
    MessageDelete,
    RoomUpdateView,
    RoomDelete,
    AboutView,
    UserProfile,
)

urlpatterns = [
    path('', HomeListView.as_view(), name='homepage'),
    path('about/', AboutView.as_view(), name='about'),
    path('room/<uuid:room_id>/', RoomDetailView.as_view(), name='room'),
    path('profile/<str:pk>/', UserProfile.as_view(), name='user_profile'),

    path('create-room/', RoomCreateView.as_view(), name='create_room'),
    path('update-room/<uuid:room_id>/', RoomUpdateView.as_view(), name='update_room'),
    path('delete-room/<uuid:room_id>/', RoomDelete.as_view(), name='delete_room'),
    path('delete-message/<uuid:id>/', MessageDelete.as_view(), name='delete_message'),
]
