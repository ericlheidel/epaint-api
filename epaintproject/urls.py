from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from epaintapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"paints", Paints, "paint")
router.register(r"profile", Profiles, "profile")
router.register(r"painttypes", PaintTypes, "painttype")
router.register(r"orders", Orders, "order")
router.register(r"sizes", Sizes, "size")
urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
