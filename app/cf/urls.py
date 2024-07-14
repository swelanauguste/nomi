from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("transactions.urls")),
    path("", include("pwa.urls")),
    path("accounts/", include("allauth.urls")),
]
