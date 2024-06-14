from django.urls import path, include
from rest_framework import routers

from security import views

router = routers.DefaultRouter()
router.register(r'users', views.ChannelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]