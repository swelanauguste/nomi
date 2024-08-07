from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.update_profile, name="profile"),
    path("create_user/", views.create_user, name="create_user"),
    path("register/<uuid:key>/", views.unique_registration, name="unique_registration"),
]
