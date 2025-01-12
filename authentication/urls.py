from django.urls import path
from django.contrib.auth.views import *
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),

    path('login/', views.login, name='login'),

    path('google-login/', views.google_login, name='google_login'),

    path('logout/', views.logout, name='logout'),

    path('password_change/', PasswordChangeView.as_view(
            template_name='authentication/password_change.html',
        ), name='password_change'),

    path('password_change_done/', PasswordChangeDoneView.as_view(
            template_name='authentication/password_change_done.html',
        ), name='password_change_done'),

    path('profile/', views.profile, name='profile'),

    path('settings/', views.settings, name='settings'),

path('manage_address/', views.manage_address, name='manage_address'),
path('manage_address/<int:address_id>/', views.manage_address, name='manage_address'),

    path('delete-account/', views.delete_account, name='delete_account'),


]
