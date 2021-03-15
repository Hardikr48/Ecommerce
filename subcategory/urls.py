from rest_framework.routers import DefaultRouter
from .views import SubCategoryViewSet

router = DefaultRouter()
router.register(r'subcategory', SubCategoryViewSet, basename='subcategory')
urlpatterns = router.urls
