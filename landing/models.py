from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class State(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.title()


class Train(models.Model):
    image = models.URLField(blank=True)
    capacity = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.title()


class Class(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return f"{self.name}  class".title()


class Seat(models.Model):
    cls = models.ForeignKey(Class, models.CASCADE)
    train = models.ForeignKey(Train, models.CASCADE)

    class Meta:
        ordering = ["cls"]

    def __str__(self):
        return f"{self.cls} - {self.train}"


class Schedule(models.Model):
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    scheduled_date = models.DateField()
    distance = models.FloatField(default=0)
    train = models.ForeignKey(Train, models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    to_state = models.ForeignKey(State, models.CASCADE, related_name="arrivals")
    from_state = models.ForeignKey(State, models.CASCADE, related_name="departures")

    class Meta:
        ordering = ["scheduled_date"]

    def time_difference(self):
        # Convert the TimeField values to datetime objects for calculation
        arrival_datetime = datetime.combine(datetime.today(), self.arrival_time)
        departure_datetime = datetime.combine(datetime.today(), self.departure_time)

        # Calculate the time difference
        difference = arrival_datetime - departure_datetime

        # Convert the timedelta object to a string representation (e.g., '1 day, 3:45:00')
        return str(difference)

    def clean(self):
        if self.from_state == self.to_state:
            raise ValidationError("Departure and arrival state cannot be the same")
        return super().clean()

    def __str__(self):
        return f"{self.train} - {self.scheduled_date}"
