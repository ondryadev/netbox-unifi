from __future__ import annotations

from django.urls import path

from netbox_unifi import views

app_name = "netbox_unifi_api"

urlpatterns = (
    path("status/", views.api_status_view, name="status"),
    path("controllers/<int:pk>/test/", views.controller_test_api_view, name="controller-test"),
)
