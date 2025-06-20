from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

app_name = 'accounts'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('signup/', views.SignupUser.as_view(), name='signup'),
    path('profile/', views.MyUserProfile.as_view(), name='profile'),

    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/',
         views.CustomPasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done'),
         ),
         name='password_reset'),
    path('password-reset/done',
         PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete'),
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
