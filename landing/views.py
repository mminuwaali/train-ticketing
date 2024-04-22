from django.urls import reverse
from django.contrib import messages
from account.models import Booking, Ticket
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from landing.models import State, Class, Schedule


def about_view(request):
    return render(request, "landing/about.html")


def contact_view(request):
    return render(request, "landing/contact.html")


def index_view(request):
    if request.method == "POST":
        url = reverse("landing:search-view")

        _to = request.POST.get("to")
        date = request.POST.get("date")
        _from = request.POST.get("from")
        _class = request.POST.get("class")

        return redirect(url + f"?class={_class}&date={date}&to={_to}&from={_from}")

    states = State.objects.all()
    classes = Class.objects.all()
    schedules = Schedule.objects.filter(scheduled_date__gte=datetime.today())[:8]

    context = {"states": states, "classes": classes, "schedules": schedules}
    return render(request, "landing/index.html", context)


def search_view(request):
    _to = request.GET.get("to")
    date = request.GET.get("date")
    _from = request.GET.get("from")
    _class = request.GET.get("class")

    schedules = Schedule.objects.filter(
        from_state__name=_from, to_state__name=_to, scheduled_date=date
    )

    context = {
        "to": _to,
        "date": date,
        "from": _from,
        "class": _class,
        "schedules": schedules,
    }
    return render(request, "landing/search.html", context)


def booking_view(request, id):
    classes = Class.objects.all()
    schedule = Schedule.objects.get(id=id)
    vacant_seats = schedule.train.seat_set.exclude(ticket__booking__schedule=schedule)

    for cls in classes:
        cls.seats = vacant_seats.filter(cls=cls)

    context = {"schedule": schedule, "classes": classes}
    return render(request, "booking/index.html", context)


def confirm_booking_view(request, id):
    if request.method == "POST":
        classes = Class.objects.all()
        schedule = Schedule.objects.get(id=id)

        booking = Booking.objects.create(user=request.user, schedule=schedule)
        vacant_seats = schedule.train.seat_set.exclude(
            ticket__booking__schedule=schedule
        )

        for cls in classes:
            vacant = vacant_seats.filter(cls=cls)
            seats_count = int(request.POST.get(f"{cls.id}", 0))

            if seats_count and vacant.exists():

                Ticket.objects.bulk_create(
                    [
                        Ticket(
                            booking=booking,
                            seat=vacant.first(),
                            # train=schedule.train,
                            price=float(schedule.distance) * float(cls.price),
                        )
                        for i in range(seats_count)
                    ]
                )

    messages.success(request, "Your tickets have been booked successfully")
    messages.success(request, "Check your dashboard for more information")

    return redirect("landing:index-view")
    return redirect(request.META.get("HTTP_REFERER", "landing:index-view"))
