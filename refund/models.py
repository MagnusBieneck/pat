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
        return float(sum([receipt.amount for receipt in Receipt.objects.filter(refund=self)]))


class Receipt(models.Model):
    """Model representing a receipt."""
    refund = models.ForeignKey("Refund", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=8)

    # Add document field here!
