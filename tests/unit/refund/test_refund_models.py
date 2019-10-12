"""Module containing tests for the refund models."""
from datetime import datetime

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

    assert refund.is_approved is False
    refund.approved = datetime.now()
    assert refund.is_approved is True

    assert refund.is_processed is False
    refund.processed = datetime.now()
    assert refund.is_processed is True


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
    staff_user_one = User(username="staff_user_one", is_staff=True)
    staff_user_one.save()
    staff_user_two = User(username="staff_user_two", is_staff=True)
    staff_user_two.save()
    super_user = User(username="super_user", is_superuser=True)
    super_user.save()

    request_one = Refund(**refund_dict, user=user_one, department_leader=staff_user_one)
    request_one.save()
    request_two = Refund(**refund_dict, user=user_two, department_leader=staff_user_two)
    request_two.save()
    request_three = Refund(**refund_dict, user=staff_user_one, department_leader=staff_user_one)
    request_three.save()
    request_four = Refund(**refund_dict, user=staff_user_two, department_leader=staff_user_two)
    request_four.save()
    request_five = Refund(**refund_dict, user=super_user, department_leader=staff_user_two)
    request_five.save()

    # Check requests before any processing
    assert list(Refund.get_all(user_one)) == [request_one]
    assert list(Refund.get_all(user_two)) == [request_two]
    assert list(Refund.get_all(staff_user_one)) == [request_one, request_three]
    assert list(Refund.get_all(staff_user_two)) == [request_two, request_four, request_five]
    assert list(Refund.get_all(super_user)) == [request_five]

    # TO DO: Check requests after processing


@pytest.mark.django_db
def test_get_latest_account_info():
    """Test that the correct account info are returned based on the latest request."""
    user = User(username="user")
    user.save()

    assert Refund.get_latest_account_info(user) is None

    account_info_one = {
        "bank_account_owner": "Mr Smith",
        "bank_account_iban": "DE1234567890",
        "bank_account_bic": "ABCDEFG1HIJ"
    }

    Refund.objects.create(date_submitted="2019-10-01", **account_info_one,
                          refund_type="bank_account", user=user)
    assert Refund.get_latest_account_info(user) == tuple(account_info_one.values())

    Refund.objects.create(date_submitted="2019-10-02",
                          refund_type="cash", user=user)
    assert Refund.get_latest_account_info(user) == tuple(account_info_one.values())

    account_info_two = {
        "bank_account_owner": "Mr Wilson",
        "bank_account_iban": "DE0987654321",
        "bank_account_bic": "JIHGFEDCBA"
    }

    Refund.objects.create(date_submitted="2019-10-03", **account_info_two,
                          refund_type="bank_account", user=user)
    assert Refund.get_latest_account_info(user) == tuple(account_info_two.values())
