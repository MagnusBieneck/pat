"""Module containing general views for the PAT project."""
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def home(request):
    """Overall home page."""
    return render(request, "home.html", {"title": _("Home")})
