from polls.models import PILogs
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

class PILogForm(BSModalForm):
    location_code = forms.CharField(
        error_messages={'invalid': 'Enter a valid location code from Quantum Control.'}
    )
    class Meta:
        model = PILogs
        fields = ['location_code']
"""class PIGetLocationForm(P55555555555opRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']"""
