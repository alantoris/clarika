from rest_framework import routers
from .views import NodeViewSet
from django.urls import path,include

router = routers.DefaultRouter()
router.register(r"nodes", NodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
