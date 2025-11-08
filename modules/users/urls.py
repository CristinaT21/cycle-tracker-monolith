"""
URL routing for the Users module.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile endpoints
    path('me/', views.get_current_user, name='current_user'),
    path('me/update/', views.update_user_profile, name='update_profile'),
    path('me/preferences/', views.update_user_preferences, name='update_preferences'),
    path('me/change-password/', views.change_password, name='change_password'),
]
