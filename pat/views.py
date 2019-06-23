"""Module containing general views for the PAT project."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@login_required
def home(request):
    """Overall home page."""
    return render(request, "home.html", {"title": _("Home")})
