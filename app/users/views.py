from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, CustomUserCreationForm
from .models import Profile


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
