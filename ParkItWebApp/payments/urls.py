from django.urls import path

from ParkItWebApp.payments.views import PaymentsView

urlpatterns = [
    path('payments/<int:pk>/', PaymentsView.as_view(), name='payments_page'),
]