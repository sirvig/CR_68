from django import forms
from models import *

class DonationForm(forms.Form):
    FREQUENCY_CHOICES = (
        ('1','One-time'),
        ('2','Monthly'),
    )
    
    name         = forms.CharField(widget=forms.TextInput(attrs={'size': '35'}))
    anon         = forms.BooleanField(required=False)
    emailaddress = forms.EmailField(widget=forms.TextInput(attrs={'size': '35'}), label="Email Address")
    amount       = forms.CharField(widget=forms.TextInput(attrs={'size': '10'}))
    centername   = forms.CharField(widget=forms.HiddenInput())
    frequency    = forms.CharField(widget=forms.HiddenInput())
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        # strip $
        amount = amount.strip('$')
        # strip commas
        amount = amount.strip(',')
        # strip everything right of period
        amount = amount.split('.')[0]
        
        return amount