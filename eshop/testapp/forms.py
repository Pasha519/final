from django import forms
from testapp.models import Order
from django.contrib.auth.models import User
from django.core import validators

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username",'first_name','last_name','email','password']


class OrderForm(forms.ModelForm):
    # quantity = forms.IntegerField(disabled=True)
    price = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    address = forms.CharField(validators=[validators.MinLengthValidator(10)])
    phone = forms.CharField(validators=[validators.MinLengthValidator(10)])
    
    class Meta:
        model = Order 
        fields = "__all__"

class SearchForm(forms.Form):
    search = forms.CharField(max_length=10,label="",initial="Search Item")
