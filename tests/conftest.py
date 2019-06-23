"""Module containing global fixtures for all types of tests."""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from refund.models import Refund

REFUND_DICT = {
        "date_submitted": "2019-06-06",
        "department_leader": "John Doe",
        "account": "Dunno",
        "cost_centre": "General Expenses",
        "project": "Conference",
        "refund_type": "cash",
        "bank_account_owner": "Mr Smith",
        "bank_account_iban": "DE1234567890",
        "bank_account_bic": "ABCDEFG1HIJ"
    }

_CLIENT = Client()
# pylint:disable=redefined-outer-name,unused-argument


@pytest.fixture
def refund_dict():
    """Returns a dict with refund parameters."""
    return REFUND_DICT


# pylint: disable=redefined-outer-name
@pytest.fixture
def refund(refund_dict):
    """Returns a refund instance."""
    return Refund(**refund_dict)


@pytest.fixture
def client():
    """Return a Django test client."""
    return _CLIENT


@pytest.fixture
def login(client):
    """Login as a user."""
    username = "John Doe"
    password = "123456"

    user = User.objects.create_user(username, password=password)
    user.save()

    assert client.login(username=username, password=password)

    return user
