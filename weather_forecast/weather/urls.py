from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet

router = DefaultRouter()
router.register(r'', WeatherDataViewSet, basename='weather-data')

urlpatterns = [
    path('', include(router.urls)),
]