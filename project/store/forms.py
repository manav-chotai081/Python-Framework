from django import forms
from django.contrib.auth.models import User
from .models import CustomerProfile, Product

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    customer_type = forms.ChoiceField(
        choices=CustomerProfile.CUSTOMER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Choose Wholesale if you are an electrician or contractor"
    )
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    business_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agency/Electrician Name (if contractor)'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class ProductQuickUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['retail_price', 'wholesale_price', 'stock']
        widgets = {
            'retail_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'wholesale_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }
