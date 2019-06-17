"""Module containing forms for the refund app."""
from django import forms
from refund.models import Refund


class RefundForm(forms.ModelForm):
    """The basic refund Form Class."""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta class connecting the model to the model form."""
        model = Refund
        fields = [
            "department_leader",
            "account",
            "cost_centre",
            "project",
            "refund_type",
            "bank_account_owner",
            "bank_account_iban",
            "bank_account_bic"
        ]

        for i in range(10):
            fields.append("receipt_{}_picture".format(i))
            fields.append("receipt_{}_amount".format(i))

        localized_fields = "__all__"
