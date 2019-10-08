"""Module containing tests for the refund form."""
import pytest
from refund.forms import RefundForm


# pylint: disable=no-member
@pytest.mark.django_db
def test_disabled():
    """Test basic functionality of the Refund model."""
    form = RefundForm()
    form.disable()

    for _, field in form.fields.items():
        assert field.disabled
