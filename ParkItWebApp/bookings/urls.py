from django.urls import path

from ParkItWebApp.bookings.views import DeleteBookingsView, CreateBookingsView, BookingsView

urlpatterns = [
    path('booking/delete/<int:pk>/', DeleteBookingsView.as_view(), name="delete-bookings-page"),
    path('booking/create/<int:parking_spot_id>/', CreateBookingsView.as_view(), name="create-bookings-page"),
    path('bookings/<int:pk>/', BookingsView.as_view(), name="bookings_view"),
]