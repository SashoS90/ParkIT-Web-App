from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Booking
from .forms import CreateBookingForm
from ..common.utils import get_common_data
from ..parking_spots.models import ParkingSpot


UserModel = get_user_model()

class DeleteBookingsView(DeleteView):
    model = Booking
    template_name = "delete-bookings.html"

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse("listings_view", args=[user_id])


class CreateBookingsView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Booking
    form_class = CreateBookingForm
    template_name = 'create_booking.html'
    success_url = reverse_lazy('bookings_view')
    success_message = "Booking was created successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_parking_spot_id = self.kwargs.get('parking_spot_id')
        if selected_parking_spot_id:
            parking_spot = get_object_or_404(ParkingSpot, id=selected_parking_spot_id)
            context['parking_spot'] = parking_spot
            context['hourly_rate'] = parking_spot.hourly_rate

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        selected_parking_spot_id = self.kwargs.get('parking_spot_id')
        if selected_parking_spot_id:
            try:
                selected_parking_spot = ParkingSpot.objects.get(id=selected_parking_spot_id)
                form.instance.parking_spot = selected_parking_spot

                if selected_parking_spot.owner == self.request.user:
                    form.add_error(None, "You cannot book your own parking spot.")
                    return self.form_invalid(form)

            except ParkingSpot.DoesNotExist:
                pass

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bookings_view', args=[self.request.user.id])


class BookingsView(ListView):
    model = UserModel
    template_name = "dashboard_bookings.html"

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.filter(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user
        common_data = get_common_data(user_profile)
        context.update(common_data)

        return context