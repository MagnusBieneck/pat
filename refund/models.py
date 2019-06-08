"""Module containing models for the refund app."""
from django.db import models

REFUND_TYPES = [
    ("cash", "Bargeld"),
    ("bank_account", "Überweisung"),
    ("amazon", "Amazon-Account"),
    ("credit_card", "Kreditkarte")
]


class Refund(models.Model):
    """Model representing an expense refund form."""
    date_submitted = models.DateField()
    department_leader = models.CharField(max_length=128)
    account = models.CharField(max_length=128)
    cost_centre = models.CharField(max_length=128)
    project = models.CharField(blank=True, null=True, max_length=256)

    refund_type = models.TextField(choices=REFUND_TYPES)
    bank_account_owner = models.CharField(blank=True, null=True, max_length=128)
    bank_account_iban = models.CharField(blank=True, null=True, max_length=128)
    bank_account_bic = models.CharField(blank=True, null=True, max_length=128)

    # Receipt fields
    receipt_0_picture = models.FileField(default=None, null=True)
    receipt_0_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_1_picture = models.FileField(default=None, null=True)
    receipt_1_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_2_picture = models.FileField(default=None, null=True)
    receipt_2_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_3_picture = models.FileField(default=None, null=True)
    receipt_3_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_4_picture = models.FileField(default=None, null=True)
    receipt_4_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_5_picture = models.FileField(default=None, null=True)
    receipt_5_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_6_picture = models.FileField(default=None, null=True)
    receipt_6_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_7_picture = models.FileField(default=None, null=True)
    receipt_7_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_8_picture = models.FileField(default=None, null=True)
    receipt_8_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_9_picture = models.FileField(default=None, null=True)
    receipt_9_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
