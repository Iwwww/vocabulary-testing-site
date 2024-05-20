from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from .settings import env

urlpatterns = i18n_patterns(
    path("", include("polls.urls")),
    path("admin/", admin.site.urls),
)
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r"rosetta/", include("rosetta.urls")),
    ]


if env.bool("DEBUG", True):
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
