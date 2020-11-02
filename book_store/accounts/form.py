from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'signup__input', 'name': 'username', 'id': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'signup__input', 'name': 'username', 'id': 'username'})
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'signup__input', 'name': 'username', 'id': 'username'}))

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'signup__input', 'name': 'username', 'id': 'username'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'signup__input', 'name': 'username', 'id': 'username'})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'signup__input', 'name': 'username', 'id': 'username'})
    )

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        conf_pass = self.cleaned_data.get('confirm_password')
        if password != conf_pass:
            raise forms.ValidationError("رمز عبور یکسان نیست ")

        return data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("نام کاربری وجود دارد ")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is already taken")
        return email
