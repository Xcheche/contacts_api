from django.urls import path
from .views import (RegisterView, LoginView, 
                    PasswordResetRequestView, PasswordResetConfirmView, api_overview)

urlpatterns = [
    path('', api_overview, name='api_overview'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
