
from django import forms
from .models import VolunteerProfile


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = ['urgency_of_need', 'past_donations']

