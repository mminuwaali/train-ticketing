from . import models
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(models.State)
class StateAdmin(ImportExportModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "latitude", "longitude"]


@admin.register(models.Train)
class TrainAdmin(ImportExportModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "capacity"]


@admin.register(models.Class)
class ClassAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "price", "updated_at", "created_at"]


@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ["cls", "train"]
    search_fields = ["cls", "train"]


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["train", "scheduled_date", "departure_time", "arrival_time"]
    search_fields = ["train", "scheduled_date", "departure_time", "arrival_time"]
