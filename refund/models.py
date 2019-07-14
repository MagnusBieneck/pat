"""Module containing models for the refund app."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

REFUND_TYPES = [
    ("cash", "Bargeld"),
    ("bank_account", "Überweisung"),
    ("amazon", "Amazon-Account"),
    ("credit_card", "Kreditkarte")
]


class Refund(models.Model):
    """Model representing an expense refund form."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_submitted = models.DateField(_("Date Submitted"))
    department_leader = models.CharField(_("Department Leader"), max_length=128)
    cost_centre = models.CharField(_("Cost Centre"), max_length=128)
    project = models.CharField(_("Project"), blank=True, null=True, max_length=256)

    refund_type = models.TextField(_("Refund Type"), choices=REFUND_TYPES)
    bank_account_owner = models.CharField(_("Bank Account Owner"), blank=True, null=True,
                                          max_length=128)
    bank_account_iban = models.CharField(_("Bank Account IBAN"), blank=True, null=True,
                                         max_length=128)
    bank_account_bic = models.CharField(_("Bank Account BIC"), blank=True, null=True,
                                        max_length=128)

    file_field_attributes = {"default": None, "null": True, "blank": True}
    decimal_field_attributes = {"max_digits": 10, "decimal_places": 2, "default": 0, "blank": True}

    # Receipt fields
    receipt_0_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_0_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_1_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_1_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_2_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_2_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_3_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_3_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_4_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_4_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_5_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_5_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_6_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_6_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_7_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_7_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_8_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_8_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)
    receipt_9_picture = models.FileField(_("Receipt"), **file_field_attributes)
    receipt_9_amount = models.DecimalField(_("Sum"), **decimal_field_attributes)

    def __str__(self):
        """String representation of the Refund object."""
        return "{} for {} ({} - {})".format(
            self.amount,
            self.project or "Unknown project",
            self.department_leader,
            self.cost_centre
        )

    @property
    def amount(self):
        """Return the sum of all receipts belonging to this refund."""
        # pylint: disable=no-member
        return float(sum([
            self.receipt_0_amount,
            self.receipt_1_amount,
            self.receipt_2_amount,
            self.receipt_3_amount,
            self.receipt_4_amount,
            self.receipt_5_amount,
            self.receipt_6_amount,
            self.receipt_7_amount,
            self.receipt_8_amount,
            self.receipt_9_amount
        ]))

    @property
    def requester(self):
        """Return the first and last name of the requester."""
        # pylint: disable=no-member
        return "{} {}".format(self.user.first_name, self.user.last_name)

    @staticmethod
    def get_all(current_user):
        """Return all requests based on the current user rights.

        Args:
            current_user (django.contrib.auth.models.User): User currently logged in (from request).

        Returns:
            list[Refund]: List of 0 to n refund objects.
        """
        if current_user.is_staff:
            return Refund.objects.all()  # pylint: disable=no-member

        return Refund.objects.filter(user=current_user).all()  # pylint: disable=no-member
