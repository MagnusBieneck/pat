"""Module containing general views for the PAT project."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import static


@login_required
def home(request):
    """Overall home page."""
    return render(request, "home.html", {"title": _("Home")})


@login_required
def serve(request, path, document_root=None):
    """Wrapper for static file serving, requires the user to be logged in."""
    return static.serve(request, path, document_root, show_indexes=False)
