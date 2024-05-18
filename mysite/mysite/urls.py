from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .settings import env

urlpatterns = [
    path("", include("polls.urls")),
    path("admin/", admin.site.urls),
]

if env.bool("DEBUG", True):
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
