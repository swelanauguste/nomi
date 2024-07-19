from django import forms

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }
