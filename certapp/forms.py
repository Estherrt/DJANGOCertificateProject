from django import forms
from .models import Participant

class PForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=["name","course","email"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'course': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'email': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }

