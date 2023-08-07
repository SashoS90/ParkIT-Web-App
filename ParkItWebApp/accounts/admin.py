from django.contrib import admin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'email__istartswith', 'username__istartswith']
    ordering = ['username']