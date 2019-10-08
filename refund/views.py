"""Module containing views for the Refund app."""
from datetime import date, datetime, timezone
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

    context.update({"title": _("Refund Overview"), "data": data, "is_staff": request.user.is_staff})
    return render(request, "refund/index.html", context)


def _alert(request, alert_type, alert_message):
    """Helper function that redirects to the refund index page and shows an alert."""
    return index(request, context={"alert": {"type": alert_type, "message": alert_message}})


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


@login_required
def request_edit(request, request_id):
    """The request form edit view."""
    refund = Refund.objects.get(id=request_id)  # pylint: disable=no-member
    form = RefundForm(instance=refund)
    form.disable()

    data = {
        "form": form,
        "title": _("Expense Refund"),
        "edit": True,
        "approval_right": request.user == form.instance.department_leader and request.user.is_staff,
        "approved": refund.is_approved,
        "process_right": request.user.is_superuser and refund.is_approved,
        "request_id": request_id
    }

    return render(request, "refund/request_form.html", data)


@login_required
def request_approve(request, request_id):
    """The request approve view."""
    refund = Refund.objects.get(id=request_id)  # pylint: disable=no-member

    if not request.user.is_staff:
        return _alert(request, "danger",
                      _("You cannot approve any requests as you are no department leader."))

    if refund.department_leader != request.user:
        return _alert(request, "danger",
                      _("You can only approve requests within your own department."))

    if refund.is_approved:
        return _alert(request, "warning", _("This request has already been approved."))

    refund.approved = datetime.now(tz=timezone.utc)
    refund.save()
    return _alert(request, "success", _("The request has been successfully approved."))


@login_required
def request_process(request, request_id):
    """The request process view."""
    refund = Refund.objects.get(id=request_id)  # pylint: disable=no-member

    if not request.user.is_superuser:
        return _alert(request, "danger",
                      _("You cannot approve any requests as you are no finance leader."))

    if not refund.is_approved:
        return _alert(request, "warning",
                      _("This request must be approved before it can be processed."))

    if refund.is_processed:
        return _alert(request, "warning", _("This request has already been processed."))

    refund.processed = datetime.now(tz=timezone.utc)
    refund.save()
    return _alert(request, "success", _("The request has been successfully processed."))
