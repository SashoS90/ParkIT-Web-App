from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from .validators import contains_only_letters, starts_with_capital, phone_number_validator


class UserProfile(auth_models.AbstractUser):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 50
    PHONE_NUMBER_MAX_LENGTH = 13
    PHONE_NUMBER_MIN_LENGTH = 10

    username = models.CharField(blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH,
                                  blank=False,
                                  null=False,
                                  validators=[MinLengthValidator(FIRST_NAME_MIN_LENGTH),
                                              contains_only_letters,
                                              starts_with_capital], )
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH,
                                 blank=False,
                                 null=False,
                                 validators=[MinLengthValidator(LAST_NAME_MIN_LENGTH),
                                             contains_only_letters,
                                             starts_with_capital])
    email = models.EmailField(blank=False,
                              null=False,
                              unique=True)
    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH,
                                    validators=[phone_number_validator, MinLengthValidator(PHONE_NUMBER_MIN_LENGTH)],
                                    unique=True)
    profile_picture = models.ImageField(blank=True,
                                        null=True, upload_to='profile_pictures/')

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
