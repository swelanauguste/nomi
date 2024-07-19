from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm
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





