from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'authentication'

# Router for the VendeurProfileAdminViewSet (admin seller profiles management)
router = DefaultRouter()
router.register(r'vendeur-profiles', views.VendeurProfileAdminViewSet, basename='vendeurprofile')

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User profile endpoints
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/vendeur/', views.VendeurProfileView.as_view(), name='vendeur-profile'),
    path('profile/acheteur/', views.AcheteurProfileView.as_view(), name='acheteur-profile'),

    # Password change
    path('change-password/', views.change_password_view, name='change-password'),

    # Public sellers endpoints
    path('vendeurs/', views.VendeurListView.as_view(), name='vendeurs-list'),
    path('vendeurs/<int:vendeur_id>/', views.vendeur_detail_view, name='vendeur-detail'),

    # Admin user management endpoints
    path('users/', views.UserListView.as_view(), name='users-list'),  # List all users (admin)
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),  # Retrieve/update/delete user (admin)
    path('users/<int:user_id>/status/', views.update_user_status, name='user-update-status'),  # Patch status
    path('users/<int:user_id>/reset-password/', views.AdminResetPasswordView.as_view(), name='admin-reset-password'),  # Admin reset password

    # Include router urls (e.g. for seller profiles admin actions)
    path('', include(router.urls)),
]
