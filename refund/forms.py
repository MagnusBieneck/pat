"""Module containing forms for the refund app."""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from localflavor.generic.validators import BICValidator, IBANValidator

from refund.models import Refund


class RefundForm(forms.ModelForm):
    """The basic refund Form Class."""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta class connecting the model to the model form."""
        model = Refund
        fields = [
            "department_leader",
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

    def clean(self):
        """Clean and validate the form data."""
        data = super().clean()

        # When `bank account` is chosen as refund type, three additional fields must be validated:
        # Bank account owner, IBAN and BIC.
        if data.get("refund_type") == "bank_account":
            if not data.get("bank_account_owner"):
                self.add_error("bank_account_owner", _("This field is required."))

            if data.get("bank_account_iban"):
                iban_validator = IBANValidator()
                try:
                    iban_validator(data.get("bank_account_iban"))
                except ValidationError:
                    self.add_error("bank_account_iban", _("A valid IBAN is required."))
            else:
                self.add_error("bank_account_iban", _("This field is required."))

            if data.get("bank_account_bic"):
                bic_validator = BICValidator()
                try:
                    bic_validator(data.get("bank_account_bic"))
                except ValidationError:
                    self.add_error("bank_account_bic", _("A valid BIC is required."))
            else:
                self.add_error("bank_account_bic", _("This field is required."))

        # Receipt validation
        if not any([data.get("receipt_{}_picture".format(i)) for i in range(10)]):
            self.add_error("receipt_0_picture", _("At least one receipt is required."))

        for i in range(10):
            if data.get(f"receipt_{i}_picture") and not data.get(f"receipt_{i}_amount"):
                self.add_error(f"receipt_{i}_picture",
                               _("The amount for this receipt is required."))
            elif data.get(f"receipt_{i}_amount") and not data.get(f"receipt_{i}_picture"):
                self.add_error(f"receipt_{i}_amount", _("The receipt for this amount is required."))
