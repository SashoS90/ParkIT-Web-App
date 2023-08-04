from django.shortcuts import render
from django.views.generic import ListView

from ParkItWebApp.common.utils import get_common_data
from ParkItWebApp.reviews.models import Review


class ReviewsListView(ListView):
    model = Review
    template_name = "reviews_list_page.html"
    context_object_name = "user_reviews"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Review.objects.filter(parking_spot__owner=user).order_by("id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user
        common_data = get_common_data(user_profile)
        context.update(common_data)

        return context
