from django.urls import path
from django.contrib.auth import views as auth_views

from ParkItWebApp.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, ProfileView, DashboardView, \
    EditProfileView, ChangePasswordView, PasswordChangeCompletedView, DeleteProfileView, ListingsView, BookingsView, \
    PaymentsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_page'),
    path('login/', LoginUserView.as_view(), name='login_page'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/<int:pk>/', DashboardView.as_view(), name='dashboard'),
    path('profile/<int:pk>/edit/', EditProfileView.as_view(), name='edit_profile_page'),
    path('accounts/password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeCompletedView.as_view(), name='password_change_completed'),
    path('profile/<int:pk>/delete', DeleteProfileView.as_view(), name='delete_profile_page'),
    path('profile/<int:pk>/listings/', ListingsView.as_view(), name='listings_view'),
    path('profile/<int:pk>/bookings/', BookingsView.as_view(), name='bookings_view'),
    path('profile/<int:pk>/payments/', PaymentsView.as_view(), name='payments_page'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_page'),
]
