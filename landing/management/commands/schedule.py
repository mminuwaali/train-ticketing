import calendar
from random import randint
from landing import models
from geopy.distance import geodesic
from datetime import time, timedelta, datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a schedule for all trains"

    def add_arguments(self, parser):
        parser.add_argument(
            "num",
            type=int,
            nargs="?",
            default=50,
            help="Number of schedules (default 50)",
        )
        parser.add_argument(
            "--months",
            type=int,
            default=1,
            help="Number of months for schedules (default 1)",
        )

    def handle(self, *args, **options):
        num = options.get("num", 50)
        months = options.get("months", 1)

        trains = models.Train.objects.all()
        states = models.State.objects.all()

        schedules = []

        # Average speed of a train in Nigeria (km/h)
        average_speed = 80

        # Get the current date
        now = datetime.now()

        # Get the last day of the next month
        _, last_day = calendar.monthrange(now.year, now.month + months)

        for _ in range(num):
            train = trains.order_by("?").first()
            departure_time = time(randint(6, 15), randint(0, 59))
            scheduled_date = datetime(
                now.year,
                now.month + months,
                randint(now.day, last_day),
            ).date()  # Random date in the next month

            to_state = states.order_by("?").first()
            from_state = states.exclude(id=to_state.id).order_by("?").first()

            # Calculate distance between states
            distance = geodesic(
                (from_state.latitude, from_state.longitude),
                (to_state.latitude, to_state.longitude),
            ).kilometers

            # Calculate travel time based on distance and average speed
            travel_time_hours = (departure_time.hour + distance / average_speed) % 24
            arrival_time = time(int(travel_time_hours), departure_time.minute)

            # Create the Schedule instance
            schedule = models.Schedule(
                train=train,
                distance=distance,
                to_state=to_state,
                from_state=from_state,
                arrival_time=arrival_time,
                departure_time=departure_time,
                scheduled_date=scheduled_date,
            )
            schedules.append(schedule)

        models.Schedule.objects.bulk_create(schedules)

        self.stdout.write(
            self.style.SUCCESS(f"Created {num} schedules for {months} month(s)")
        )
