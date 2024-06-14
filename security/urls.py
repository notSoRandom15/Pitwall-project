from django.urls import path, include
from rest_framework import routers

from security import views
from security.views import KeyGenerationView

router = routers.DefaultRouter()
router.register(r'channels', views.ChannelViewSet, basename='channel')


urlpatterns = [
    path('', include(router.urls)),
    path("generate-key/", KeyGenerationView.as_view(), name='generate-key')
]