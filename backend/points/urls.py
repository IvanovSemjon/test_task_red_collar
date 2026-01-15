from rest_framework.routers import DefaultRouter
from .views import PointViewSet, PointMessageViewSet

router = DefaultRouter()
router.register(r"points", PointViewSet, basename="points")
router.register(r"messages", PointMessageViewSet, basename="point-messages")

urlpatterns = router.urls
