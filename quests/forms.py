import re
from django import forms
from .models import Session


class BookingForm(forms.Form):
    customer_name = forms.CharField(
        label="Ваше имя",
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Данила"}),
    )
    customer_email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"}),
    )
    customer_phone = forms.CharField(
        label="Телефон для связи",
        min_length=7,
        max_length=25,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 (999) 123-45-67"}),
    )
    players_count = forms.IntegerField(
        label="Количество игроков",
        min_value=2,
        max_value=12,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 2, "max": 12}),
    )
    session_id = forms.IntegerField(label="Сеанс")
    add_actor = forms.BooleanField(label="Доп. аниматор (+500 ₽)", required=False)

    def __init__(self, *args, **kwargs):
        self.quest = kwargs.pop("quest", None)
        super().__init__(*args, **kwargs)

    def clean_customer_name(self):
        name = self.cleaned_data["customer_name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Имя должно содержать минимум 2 символа.")
        return name

    def clean_customer_phone(self):
        phone = self.cleaned_data["customer_phone"].strip()
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 7 or len(digits) > 15:
            raise forms.ValidationError("Введите корректный номер телефона (от 7 до 15 цифр).")
        return phone

    def clean_players_count(self):
        count = self.cleaned_data["players_count"]
        if self.quest and count > self.quest.max_players:
            raise forms.ValidationError(
                f"Максимальное число игроков для этой комнаты — {self.quest.max_players}."
            )
        return count

    def clean_session_id(self):
        session_id = self.cleaned_data["session_id"]
        try:
            session = Session.objects.get(id=session_id, quest=self.quest)
        except Session.DoesNotExist:
            raise forms.ValidationError("Выбранный сеанс не найден.")
        if not session.is_available:
            raise forms.ValidationError("Этот сеанс уже занят. Выберите другое время.")
        self.cleaned_data["session_obj"] = session
        return session_id
