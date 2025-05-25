from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect

from apps.accounts.forms import (
    SignupUserForm,
    LoginUserForm,
    UserPasswordChangeForm,
    ProfileUserForm,
)


class LoginUser(LoginView):
    form_class = LoginUserForm
    success_url = '/'


class SignupUser(CreateView):
    form_class = SignupUserForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'registration/password_change_form.html'


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        logout(request)
        return response


class MyUserProfile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'registration/my_profile.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user
