from django import forms
from django.forms import Form
from . models import Client



class SignUpForm(Form):
    email = forms.EmailField(max_length=128)
    phone = forms.CharField(max_length=80)
    name = forms.CharField(max_length=100)
    card_num = forms.CharField(max_length=100)
    card_type = forms.CharField(max_length=3)
    sex = forms.CharField(max_length=1)
    passwd = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Client
        fields = ('email', 'phone', 'name', 'card_num', 'card_type', 'sex', 'passwd',)
