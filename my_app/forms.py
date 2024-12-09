from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, PlantRequest, QuoteRequest

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'profile_image']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Phone validation logic here
        if phone_number:
            return phone_number
        return phone_number

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  # Add form-control class for styling
            field.help_text = ''  # Disable help text display

class PlantRequestForm(forms.ModelForm):
    class Meta:
        model = PlantRequest
        fields = ['quantity', 'delivery_address', 'phone_number']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
        }

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['service', 'first_name', 'last_name', 'email', 'phone', 'property_image', 'location', 'additional_info']
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 2}),
        }

