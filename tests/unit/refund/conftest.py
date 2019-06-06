"""Contains fixtures for the refund tests."""
import pytest
from refund.models import Refund


@pytest.fixture
def refund_dict():
    """Returns a dict with refund parameters."""
    return {
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


@pytest.fixture
def refund(refund_dict):
    """Returns a refund instance."""
    return Refund(**refund_dict)
