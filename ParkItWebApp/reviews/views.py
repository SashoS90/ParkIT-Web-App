from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from ParkItWebApp.common.utils import get_common_data
from ParkItWebApp.parking_spots.models import ParkingSpot
from ParkItWebApp.reviews.forms import CreateReviewForm
from ParkItWebApp.reviews.models import Review
from django.shortcuts import get_object_or_404


class AllReviewsListView(ListView):
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


class ParkingSpotReviewsView(ListView):
    model = Review
    template_name = "parking_spot_reviews.html"
    paginate_by = 10
    context_object_name = "parking_spot_reviews"

    def get_queryset(self):
        parking_spot = get_object_or_404(ParkingSpot, pk=self.kwargs['pk'])

        queryset = Review.objects.filter(parking_spot=parking_spot).order_by('-date_created')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['parking_spot'] = get_object_or_404(ParkingSpot, pk=self.kwargs['pk'])

        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = "create_review.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.parking_spot = ParkingSpot.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['parking_spot'] = get_object_or_404(ParkingSpot, pk=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return reverse_lazy("parking_spot_details_page", args=[self.kwargs['pk']])
