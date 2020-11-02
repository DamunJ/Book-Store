from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'signup__input', 'name': 'username','id': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'signup__input', 'name': 'username','id': 'username'})
    )
