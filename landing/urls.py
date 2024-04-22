from . import views
from django.urls import path

app_name, urlpatterns = "landing", [
    path("", views.index_view, name="index-view"),
    path("about/", views.about_view, name="about-view"),
    path("search/", views.search_view, name="search-view"),
    path("contact/", views.contact_view, name="contact-view"),
    path("<id>/booking/", views.booking_view, name="booking-view"),
    path("<id>/book/", views.confirm_booking_view, name="confirm-booking-view"),
]
