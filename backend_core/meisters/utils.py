from .models import Meister


def get_or_create_meister(**data):
    meister, created = Meister.objects.get_or_create(**data)
    if created:
        meister.save()
    else:
        pass