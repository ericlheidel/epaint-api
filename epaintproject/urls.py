from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from epaintapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"paints", Paints, "paint")

urlpatterns = [
    path("", include(router.urls)),
]
