from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(models.User)
class UserAdmin(BaseUserAdmin): ...


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter = ["email"]
    search_fields = ["name", "email"]
    list_display = ["name", "email", "phone"]


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_filter = ["status", "seat", "booking"]
    list_display = ["id", "price", "seat", "status", "booking"]


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["schedule"]
