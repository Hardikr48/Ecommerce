
from rest_framework.routers import DefaultRouter
from account.views import UserViewSet

router = DefaultRouter()
router.register(r'account', UserViewSet, basename='account')
urlpatterns = router.urls
