"""Module containing tests for the refund models."""
from django.contrib.auth.models import User
import pytest
from refund.models import Project, CostCentre, Refund


# pylint: disable=no-member
@pytest.mark.django_db
def test_refund_basic(refund, refund_dict):
    """Test basic functionality of the Refund model."""
    refund.save()

    assert refund.date_submitted == refund_dict["date_submitted"]
    assert refund.department_leader == User.objects.filter(username="john_doe").first()
    assert refund.cost_centre == CostCentre.objects.filter(name="General Expenses").first()
    assert refund.project == Project.objects.filter(name="Marketing").first()
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

    requester = User.objects.filter(username="requester").all()[0]  # pylint: disable=no-member
    assert refund.user == requester
    assert refund.requester == "Re Quester"


@pytest.mark.django_db
def test_refund_amount(refund):
    """Test that the sum of a refund is computed correctly."""
    refund.receipt_0_amount = 10.7
    refund.receipt_1_amount = 13.2
    refund.save()

    assert refund.amount == 23.9


@pytest.mark.django_db
def test_get_all(refund_dict):
    """Test that get_all returns the refund objects according to user rights."""
    user_one = User(username="user_one")
    user_one.save()
    user_two = User(username="user_two")
    user_two.save()
    staff_user = User(username="staff_user", is_staff=True)
    staff_user.save()

    request_one = Refund(**refund_dict, user=user_one)
    request_one.save()
    request_two = Refund(**refund_dict, user=user_two)
    request_two.save()

    assert list(Refund.get_all(user_one)) == [request_one]
    assert list(Refund.get_all(user_two)) == [request_two]
    assert list(Refund.get_all(staff_user)) == [request_one, request_two]
