from tkinter import EventType

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from app.models import Reservation, Event



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "placeholder": "Enter your username",
            "class": "form-control"
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your first_name',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your last_name',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })


class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat_reservation']
        # fields="__all__"


class typeForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['type']


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.label += ' *'

    class Meta:
        model = Event
        exclude = ['free_seats', 'created_by']
        fields = "__all__"
