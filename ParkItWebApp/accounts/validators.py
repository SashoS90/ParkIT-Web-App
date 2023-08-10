from django.core.exceptions import ValidationError


def starts_with_capital(value):
    if not value[0].isupper():
        raise ValidationError("Name must start with capital letter!")


def contains_only_letters(value):
    if not value.isalpha():
        raise ValidationError("Name must contain only letters!")


def phone_number_validator(value):
    valid_mobile_number_codes = ["088", "089", "098", "087"]

    if not value.startswith("0"):
        raise ValidationError("Invalid mobile number! Mobile number must start with 0!")

    if value.startswith("+") and len(value) < 13:
        raise ValidationError("Invalid phone number!")

    if value.startswith("0") and len(value) < 10:
        raise ValidationError("Invalid phone number!")

    for mobile_code in valid_mobile_number_codes:
        if value.startswith(mobile_code):
            break

    else:
        raise ValidationError("Invalid mobile operator code!")
