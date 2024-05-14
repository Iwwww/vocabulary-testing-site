from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
