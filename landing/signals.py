from . import models
from random import choice
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=models.Train)
def create_train_seats(sender, instance, created, **kwargs):
    if created:
        classes = models.Class.objects.all()
        models.Seat.objects.bulk_create(
            [
                models.Seat(train=instance, cls=choice(classes))
                for i in range(instance.capacity)
            ]
        )
    else:
        seats = instance.seat_set.all()
