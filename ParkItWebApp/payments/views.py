from django.contrib.auth import get_user_model
from django.views.generic import ListView

from ParkItWebApp.common.utils import get_common_data
from ParkItWebApp.payments.models import Payment

UserModel = get_user_model()


class PaymentsView(ListView):
    model = UserModel
    template_name = "dashboard_payments.html"
    context_object_name = "user_payments"
    paginate_by = 10
    ordering = "id"

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.filter(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user
        common_data = get_common_data(user_profile)
        context.update(common_data)

        return context
