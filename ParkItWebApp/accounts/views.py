from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from ParkItWebApp.accounts.forms import RegisterUserForm, LoginUserForm, EditProfileForm
from django.templatetags.static import static
from ParkItWebApp.common.utils import get_common_data


UserModel = get_user_model()


class RegisterUserView(CreateView):
    model = UserModel
    template_name = 'register-page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)

        return result


class LoginUserView(LoginView):
    template_name = 'login-page.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutUserView(LogoutView):
    pass


class ProfileView(DetailView):
    template_name = 'profile-page.html'
    model = UserModel

    def_profile_image = static('images/no-profile-picture.png')

    def get_profile_image(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture

        return self.def_profile_image


class DashboardView(DetailView):
    template_name = 'dashboard/dashboard.html'
    model = UserModel
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.object
        common_data = get_common_data(user_profile)
        context.update(common_data)

        return context


class EditProfileView(UpdateView):
    model = UserModel
    form_class = EditProfileForm
    template_name = "edit-profile-page.html"

    def get_success_url(self):
        return reverse_lazy("profile_page", kwargs={"pk": self.object.id})

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_completed')

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return redirect(self.get_success_url())


class PasswordChangeCompletedView(PasswordChangeDoneView):
    template_name = 'password_change_completed.html'


class DeleteProfileView(UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'delete-profile-page.html'
    success_url = reverse_lazy('home-page')

    def test_func(self):
        user = self.request.user
        profile_id = self.kwargs.get('pk')
        profile = UserModel.objects.get(pk=profile_id)
        return user == profile


class ListingsView(DetailView):
    template_name = 'dashboard/dashboard_listings.html'
    model = UserModel
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.object
        common_data = get_common_data(user_profile)
        context.update(common_data)

        return context


# class BookingsView(DetailView):
#     template_name = 'dashboard/../bookings/templates/dashboard_bookings.html'
#     model = UserModel
#     context_object_name = "user_profile"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_profile = self.object
#         common_data = get_common_data(user_profile)
#         context.update(common_data)
#
#         return context


# class PaymentsView(ListView):
#     model = UserModel
#     template_name = "dashboard/dashboard_payments.html"
#     context_object_name = "user_payments"
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Payment.objects.filter(user=user)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_profile = self.request.user
#         common_data = get_common_data(user_profile)
#         context.update(common_data)
#
#         return context
