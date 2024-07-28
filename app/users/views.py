from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm, ProfileUpdateForm, UniqueRegistrationForm
from .models import Profile, RegistrationInvitation


def unique_registration(request, key):
    # invitation = get_object_or_404(RegistrationInvitation, key=key, used=False)

    try:
        invitation = RegistrationInvitation.objects.get(key=key, used=False)
        if request.method == "POST":
            form = UniqueRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                invitation.used = True
                invitation.save()
                # login(request, user)
                return redirect("accounts")
        else:
            form = UniqueRegistrationForm()
        return render(
            request,
            "users/unique_registration.html",
            {"invitation": invitation, "form": form},
        )
    except RegistrationInvitation.DoesNotExist:
        return render(request, "users/invalid_key.html",)


@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {"form": form}
    return render(request, "users/update_profile.html", context)


def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect("profile")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "users/create_user.html", context)
