from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from zones import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'service-areas', views.ServiceAreaViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
