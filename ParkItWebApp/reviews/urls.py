from django.urls import path

from ParkItWebApp.reviews.views import ReviewsListView

urlpatterns = [
    path('reviews/<int:pk>/', ReviewsListView.as_view(), name='reviews_page'),
]