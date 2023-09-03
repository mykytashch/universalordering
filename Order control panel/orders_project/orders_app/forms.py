# forms.py

from django import forms

class MasterCodeForm(forms.Form):
    master_code = forms.CharField(label='Master Code', max_length=100)
