from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate


class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']



class AdminLoginForm(AuthenticationForm):
  def clean(self):
    cleaned_data = super().clean()
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')

    if username and password:
      user = authenticate(username=username, password=password)
      if user is None:
        raise forms.ValidationError("Invalid login credentials.")
      if not user.is_active:
        raise forms.ValidationError("This account is inactive.")
      if not user.is_superuser:
        raise forms.ValidationError("You do not have admin privileges.")
    return cleaned_data


class AdminPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
