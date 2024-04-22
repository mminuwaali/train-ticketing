import locale
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS = [(i, i) for i in ["pending", "expired", "success"]]


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Contact(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"


class Ticket(models.Model):
    price = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seat = models.ForeignKey("landing.Seat", models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    status = models.CharField(max_length=20, default="pending", choices=STATUS)
    booking = models.ForeignKey("Booking", models.CASCADE, related_name="tickets")

    @property
    def get_price(self):
        locale.setlocale(locale.LC_ALL, 'en_NG.UTF-8')
        return locale.currency(self.price, grouping=True)
        return round(self.price, 2)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} - {self.booking.user}"


class Booking(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule = models.ForeignKey("landing.schedule", models.PROTECT)

    def total_price(self):
        return sum([i.price for i in self.tickets.all()])

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.schedule}"
