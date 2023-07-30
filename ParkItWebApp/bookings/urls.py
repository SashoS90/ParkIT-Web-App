from django.urls import path

from ParkItWebApp.bookings.views import DeleteBookingsView, CreateBookingsView

urlpatterns = [
    path('booking/delete/<int:pk>/', DeleteBookingsView.as_view(), name="delete-bookings-page"),
    path('booking/create/<int:parking_spot_id>/', CreateBookingsView.as_view(), name='create-bookings-page'),
]