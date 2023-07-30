from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'username']


class LoginUserForm(auth_forms.AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        if not user:
            raise forms.ValidationError(
                "Username not found. Please enter a valid username."
            )
        super().confirm_login_allowed(user)


class EditProfileForm(forms.ModelForm):
    class Meta():
        model = UserModel
        fields = ["first_name", "last_name", "email", "phone_number", "profile_picture"]