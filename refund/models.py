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
    department_leader = models.TextField()
    account = models.TextField()
    cost_centre = models.TextField()
    project = models.TextField(blank=True, null=True)

    refund_type = models.TextField(choices=REFUND_TYPES)
    bank_account_owner = models.TextField(blank=True, null=True)
    bank_account_iban = models.TextField(blank=True, null=True)
    bank_account_bic = models.TextField(blank=True, null=True)

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
