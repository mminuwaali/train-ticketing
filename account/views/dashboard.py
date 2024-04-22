from account import models
from django.utils import timezone
from django.shortcuts import render


def index_view(request):
    bookings = models.Booking.objects.filter(user=request.user)
    tickets = models.Ticket.objects.filter(
        status="pending",
        booking__user=request.user,
        booking__schedule__scheduled_date__gte=timezone.now().date(),
    )

    context = {"bookings": bookings, "pending_tickets": tickets}
    return render(request, "dashboard/index.html", context)
