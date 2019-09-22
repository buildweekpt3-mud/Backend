from rest_framework import routers
from .api import RoomViewSet, PlayerViewSet

router = routers.DefaultRouter()
router.register('api/rooms', RoomViewSet, 'rooms')
router.register('api/players', PlayerViewSet, 'players')

urlpatterns = router.urls
