
from rest_framework.routers import DefaultRouter
from .views import OrderItemViewSet
from django.conf.urls import url

router = DefaultRouter()
router.register(r'order', OrderItemViewSet, basename='order')
urlpatterns = router.urls
