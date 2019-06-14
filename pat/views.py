"""Module containing general views for the PAT project."""
from django.shortcuts import render


def home(request):
    """Overall home page."""
    return render(request, "home.html", {"title": "Home"})
