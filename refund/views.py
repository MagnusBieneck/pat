"""Module containing views for the Refund app."""
from datetime import date
from django.shortcuts import render

from refund.forms import RefundForm
from refund.models import Refund


def index(request, context=None):
    """Overview of refund requests."""
    context = context or {}
    data = Refund.objects.all()  # pylint: disable=no-member

    context.update({"title": "Refund Overview", "data": data})
    return render(request, "refund/index.html", context)


def request_form(request):
    """The request form view."""

    if request.method == "POST":

        form = RefundForm(request.POST, request.FILES)
        if form.is_valid():

            form.instance.date_submitted = date.today()
            form.save()

            alert = {
                "type": "success",
                "message": "Your request has been successfully created."
            }

            return index(request, context={"alert": alert})

    else:

        form = RefundForm()

    return render(request, "refund/request_form.html", {"form": form, "title": "Expense refund"})
