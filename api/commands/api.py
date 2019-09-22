from commands.models import Room, Player
from rest_framework import viewsets, permissions
from .serializers import RoomSerializer, PlayerSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.none()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.all()


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.none()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.all()
