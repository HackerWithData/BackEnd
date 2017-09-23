PROFESSIONAL = 'PROFESSIONAL'
CONSUMER = 'CONSUMER'
ROLE_CHOICES = (
    (PROFESSIONAL, 'Professional'),
    (CONSUMER, 'Consumer'),
)

MALE = 'MALE'
FEMALE = 'FEMALE'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)


class UnexpectedMultipleChoice(Exception):
    pass
