from . import dashboard
from account import forms
from django.contrib import auth, messages
from django.shortcuts import render, redirect


def signout_view(request):
    auth.logout(request)
    return redirect(request.GET.get("next", "/"))


def signup_view(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)

        if form.is_valid() and form.save():
            messages.success(request, "Account created successfully")
            return redirect("account:signin-view")

        [messages.error(request, i[0]) for i in form.errors.values()]
        return redirect("account:signup-view")

    return render(request, "account/signup.html")


def signin_view(request):
    if request.method == "POST":
        user = auth.authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            auth.login(request, user)
            return redirect(request.GET.get("next", "landing:index-view"))

        messages.error(request, "Invalid credentials")
        return redirect("account:signin-view")

    return render(request, "account/signin.html")
