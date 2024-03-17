from django import forms
from collections import defaultdict
from django.contrib.auth import password_validation
from accounts.validators import UserProfileValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import Profile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name *",
        min_length=3,
        max_length=30,
        required=True,
        error_messages={
            'min_length': 'Please, add more than 3 letters for your first name.',
            'required': 'Please fill in your first name.'
        }
    )

    last_name = forms.CharField(
        label="Last Name *",
        required=True,
        min_length=3,
        max_length=30,
        error_messages={
            'min_length': 'Please, add more than 3 letters for your last name.',
            'required': 'Please fill in your last name.'
        }
    )

    email = forms.EmailField(
        label="E-mail *",
        required=True,
        error_messages={
            'required': 'Please fill in your email address.',
        }
    )

    password1 = forms.CharField(
        label="Password *",
        strip=False,
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Please enter a password.'
        }
    )

    password2 = forms.CharField(
        label="Confirm Password *",
        strip=False,
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Please confirm your password.'
        }
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email',
            'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Email already exists.', code='invalid')
            )

        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields did not match.")
        

class LoginForm(forms.Form):

    username = forms.CharField(
        label="Username",
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Passwords do not match.')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Email already exists.', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1
    

class UserProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

    class Meta:
        model = Profile
        fields = 'country', 'interests', 'bio'

        def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)
            UserProfileValidator(self.cleaned_data, ErrorClass=ValidationError)
            return super_clean

        