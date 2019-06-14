"""Module containing views for the Refund app."""
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render

from refund.forms import RefundForm


def request_form(request):
    """The request form view."""

    if request.method == "POST":

        form = RefundForm(request.POST, request.FILES)
        if form.is_valid():

            form.instance.date_submitted = date.today()
            form.save()

            return HttpResponseRedirect("/refund/form-submitted/")

    else:

        form = RefundForm()

    return render(request, "refund/request_form.html", {"form": form, "title": "Expense refund"})


def form_submitted(request):
    """The view shown after the form has been submitted."""
    return render(request, "refund/form_submitted.html", {"title": "Form submitted"})
