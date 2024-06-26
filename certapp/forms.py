from django import forms
from .models import Participant

class PForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=["name","course","email"]