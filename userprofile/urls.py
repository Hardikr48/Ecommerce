
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet


router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet, basename='userprofile')
urlpatterns = router.urls
