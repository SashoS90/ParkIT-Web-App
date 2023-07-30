from django.core.validators import RegexValidator


post_code_validator = RegexValidator(
    regex=r'^\d{4}$',
    message='Enter a valid Bulgarian postal code.'
)