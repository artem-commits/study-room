import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин/E-mail", widget=forms.TextInput())


class SignupUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован")
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput())


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин')
    email = forms.EmailField(disabled=True, label='E-mail')
    this_year = datetime.date.today().year
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))), label='Дата рождения')

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'email', 'birth_date', 'username', 'birth_date', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }