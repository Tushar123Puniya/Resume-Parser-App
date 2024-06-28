from django import forms
from .models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm_email(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        stat = User.objects.filter(email=email).exists()
        if stat:
            self.add_error('email','This email already exists')
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    
class ResumeUploadForm(forms.Form):
    resumes = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
        
class ScoreForm(forms.Form):
    resumes = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
    resumes = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': False}))
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['name','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if len(password)<8 or len(password)>15:
            self.add_error('password',"Password must be 8 to 15 charachters long")
        if password and confirm_password and password != confirm_password:
            self.add_error('password',"Passwords do not match")
        return cleaned_data

class passwordreset(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if len(password) < 8 or len(password) > 15:
                self.add_error('password', "Password must be 8 to 15 characters long")
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match")
        
        return cleaned_data
    
class Acount(forms.ModelForm):
    name = forms.CharField(label='name')
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    
    