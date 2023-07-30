from django.urls import path

from ParkItWebApp.parking_spots.views import RentParkingSpotView, EditParkingSpotView, DeleteParkingSpotView, \
    FindParkingView, ParkingSpotDetailsView

urlpatterns = [
    path('add/', RentParkingSpotView.as_view(), name='rent_parking_spot_page'),
    path('edit/<int:pk>/', EditParkingSpotView.as_view(), name='edit_parking_spot_page'),
    path('delete/<int:pk>/', DeleteParkingSpotView.as_view(), name='delete_parking_spot_page'),
    path('search/', FindParkingView.as_view(), name='find_parking_page'),
    path('view/<int:pk>/', ParkingSpotDetailsView.as_view(), name='parking_spot_details_page'),
]
