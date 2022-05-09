from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model= User
#         fields=['username','password']

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required=True
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
        self.fields['phone_number'].required=True

    class Meta(UserCreationForm.Meta):
        model=User
        fields=['username','email','first_name','last_name','phone_number']

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if email:
            qs=User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('Email already exists')
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['avatar','first_name','last_name','website_url','phone_number','bio']

 