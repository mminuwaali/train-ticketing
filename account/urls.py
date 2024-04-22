from . import views
from django.urls import path

app_name, urlpatterns = "account", [
    path("signup/", views.signup_view, name="signup-view"),
    path("signin/", views.signin_view, name="signin-view"),
    path("signout/", views.signout_view, name="signout-view"),
    path("dashboard/", views.dashboard.index_view, name="index-view"),
]
