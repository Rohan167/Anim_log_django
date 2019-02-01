from django.core.exceptions import ValidationError



def validate_name(value):
    name = value
    if len(name) < 4:
        raise ValidationError("Minimum Length 4 for name field")



GENRES = ['Bad','Worse']

def validate_genres(value):
    val = value.capitalize()
    if value in GENRES or val in GENRES:
        raise ValidationError(f'{value} is not allowed in the field')
