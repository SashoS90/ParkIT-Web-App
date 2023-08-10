from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    error_messages = {
        'password_mismatch': "The two password fields did not match.",
    }

    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )


class LoginUserForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Incorrect username or password. Please check your credentials and try again. "
            "Alternatively, create a new account."
        ),
    }

    def confirm_login_allowed(self, user):
        if user is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login'
            )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "email", "phone_number", "profile_picture"]
