import re
from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import BikeUnit, Booking

PHONE_RE = re.compile(r"^\+7\d{10}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["unit", "start_date", "end_date", "phone", "email"]
        widgets = {
            "unit": forms.HiddenInput(),
            "start_date": forms.DateInput(attrs={"type": "date", "id": "id_start_date"}),
            "end_date": forms.DateInput(attrs={"type": "date", "id": "id_end_date"}),
            "phone": forms.TextInput(attrs={"placeholder": "+79991234567", "id": "id_phone"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "id": "id_email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unit"].queryset = BikeUnit.objects.all()
        self.fields["start_date"].widget.attrs["min"] = date.today().isoformat()
        self.fields["end_date"].widget.attrs["min"] = date.today().isoformat()

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip().replace(" ", "")
        if not PHONE_RE.match(phone):
            raise ValidationError("Телефон в формате +7XXXXXXXXXX (11 цифр).")
        return phone

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not EMAIL_RE.match(email):
            raise ValidationError("Укажите корректную электронную почту.")
        return email

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        unit = cleaned.get("unit")

        if start and start < date.today():
            self.add_error("start_date", "Дата начала не может быть в прошлом.")
        if start and end and end <= start:
            self.add_error("end_date", "Дата конца должна быть позже даты начала.")
        if unit and start and end and end > start:
            overlap = Booking.objects.filter(
                unit=unit,
                status__in=[Booking.STATUS_NEW, Booking.STATUS_ISSUED],
                start_date__lt=end,
                end_date__gt=start,
            ).exclude(pk=self.instance.pk)
            if overlap.exists():
                self.add_error(None, "На выбранные даты эта единица уже забронирована.")
        return cleaned
