"""mix_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from mix_django import settings
from mix_django.router import router_catalog, router_product, router_user
from product.views import filter_cats

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('cat/characterisitcs', cache_page(60*60)(filter_cats), name='filter_cats'),

    # ==============DRF route======================
    # users
    path('users/', include(router_user.urls)),
    path('catalog/', include(router_catalog.urls)),
    path('product/', include(router_product.urls)),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
