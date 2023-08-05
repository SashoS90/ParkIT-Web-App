from django.urls import path

from ParkItWebApp.reviews.views import AllReviewsListView, ParkingSpotReviewsView, CreateReviewView

urlpatterns = [
    path('reviews/<int:pk>/', AllReviewsListView.as_view(), name='reviews_page'),
    path('parking-spot/<int:pk>/reviews/', ParkingSpotReviewsView.as_view(), name='parking_spot_reviews_page'),
    path('create-review/parking-spot/<int:pk>/', CreateReviewView.as_view(), name='create_review_page'),
]