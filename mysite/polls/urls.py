from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("testing/", views.testing, name="testing"),
    path("process-response/", views.process_response, name="process_response"),
    path("result/", views.result, name="result"),
    path("about/", views.about, name="about"),
]
