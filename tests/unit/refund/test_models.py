"""Module containing tests for the refund models."""
import pytest


@pytest.mark.django_db
def test_refund_basic(refund, refund_dict):
    """Test basic functionality of the Refund model."""
    refund.save()

    assert refund.date_submitted == refund_dict["date_submitted"]
    assert refund.department_leader == refund_dict["department_leader"]
    assert refund.account == refund_dict["account"]
    assert refund.cost_centre == refund_dict["cost_centre"]
    assert refund.project == refund_dict["project"]
    assert refund.refund_type == refund_dict["refund_type"]
    assert refund.bank_account_owner == refund_dict["bank_account_owner"]
    assert refund.bank_account_iban == refund_dict["bank_account_iban"]
    assert refund.bank_account_bic == refund_dict["bank_account_bic"]

    assert str(refund) == "{} for {} ({} - {})".format(
        refund.amount,
        refund.project or "Unknown project",
        refund.department_leader,
        refund.cost_centre
    )


@pytest.mark.django_db
def test_refund_amount(refund):
    """Test that the sum of a refund is computed correctly."""
    refund.receipt_0_amount = 10.7
    refund.receipt_1_amount = 13.2
    refund.save()

    assert refund.amount == 23.9
