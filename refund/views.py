"""Module containing views for the Refund app."""
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from refund.forms import RefundForm
from refund.models import Refund


@login_required
def index(request, context=None):
    """Overview of refund requests."""
    context = context or {}
    data = Refund.get_all(request.user)

    context.update({"title": _("Refund Overview"), "data": data})
    return render(request, "refund/index.html", context)


@login_required
def request_form(request):
    """The request form view."""

    if request.method == "POST":

        form = RefundForm(request.POST, request.FILES)
        if form.is_valid():

            form.instance.date_submitted = date.today()
            form.instance.user = request.user
            form.save()

            alert = {
                "type": "success",
                "message": _("Your request has been successfully created.")
            }

            return index(request, context={"alert": alert})

    else:

        form = RefundForm()

    return render(request, "refund/request_form.html", {"form": form, "title": _("Expense Refund")})
