from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/registration/password_reset_form.html',
        email_template_name='accounts/registration/password_reset_email.html',
        subject_template_name='accounts/registration/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password_reset_<uidb64>_<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/registration/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('profile/<int:pk>/', include([
         path('',
              views.ProfileDetails.as_view(),
              name='profile-details'),
         path('update/',
              views.UpdateProfile.as_view(),
              name='profile-update'),
         path('remove/',
              views.DeleteProfile.as_view(),
              name='profile-remove')
         ]))
]