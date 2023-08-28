from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('me/', views.profile_view, name='profile_view'),

    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path("logout/", views.logout_view, name="logout_view"),

    path('hx-send-email-confirmation/', views.hx_send_email_confirmation, name='hx_send_email_confirmation'),
]
