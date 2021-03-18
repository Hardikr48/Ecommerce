"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url 
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as authviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^product/', include('product.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^userprofile/', include('userprofile.urls')),
    url(r'^category/', include('category.urls')),
    url(r'^subcategory/', include('subcategory.urls')),
    url(r'^cartitem/', include('cartitem.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^api-token-auth/', authviews.obtain_auth_token)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)