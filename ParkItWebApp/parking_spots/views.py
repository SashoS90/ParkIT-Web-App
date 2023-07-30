from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse
from ParkItWebApp.parking_spots.forms import RentParkingSpotForm, EditParkingSpotForm
from ParkItWebApp.parking_spots.models import ParkingSpot

UserModel = get_user_model()


class RentParkingSpotView(LoginRequiredMixin, CreateView):
    model = ParkingSpot
    template_name = 'rent_parking_spot_page.html'
    form_class = RentParkingSpotForm

    def get_success_url(self):
        return reverse('listings_view', args=[self.request.user.id])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EditParkingSpotView(UpdateView):
    model = ParkingSpot
    form_class = EditParkingSpotForm
    template_name = "edit-parking-spot-page.html"

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse("listings_view", args=[user_id])

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class DeleteParkingSpotView(DeleteView):
    model = ParkingSpot
    template_name = "delete-parking-spot-page.html"

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse("listings_view", args=[user_id])


class FindParkingView(ListView):
    model = ParkingSpot
    template_name = "find-parking-page.html"
    context_object_name = "all_search_results"
    paginate_by = 10
    ordering = ["id"]

    def get_queryset(self):
        result = super(FindParkingView, self).get_queryset()
        query = self.request.GET.get("search")

        if query:
            result = ParkingSpot.objects.filter(
                Q(city__icontains=query) |
                Q(post_code__icontains=query) |
                Q(street__icontains=query) |
                Q(house_number__icontains=query)
            )

        return result


class ParkingSpotDetailsView(DetailView):
    model = ParkingSpot
    template_name = "view-parking-spot-page.html"
    context_object_name = "parking_spot"
