from django.urls import path

from ParkItWebApp.common.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home-page')
]