from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "members_list")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Ночные Охотники"}),
            "members_list": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Данила, Алексей, Мария"}
            ),
        }
