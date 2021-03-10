
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet
from django.conf.urls import url

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
urlpatterns = router.urls


# urlpatterns = [
#     url(r'^models/$', CategoryViewSet),
# ]