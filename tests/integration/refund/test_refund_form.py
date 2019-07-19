"""Module containing integration tests for the refund form."""
import os
import tempfile
import pytest

from django.conf import settings
from refund.models import Refund
from tests.conftest import REFUND_DICT

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata", "test_refund_form")
TEMP_DIR = tempfile.TemporaryDirectory()
settings.MEDIA_ROOT = TEMP_DIR.name


@pytest.mark.django_db
def test_form(login, client):  # pylint: disable=unused-argument
    """Test that the form appears correctly."""
    response = client.get("/refund/new/")

    assert response.status_code == 200
    assert any([template.name == "refund/request_form.html" for template in response.templates])


# pylint: disable=no-member, unused-argument
@pytest.mark.django_db
def test_submit(login, client, department_leader, project, cost_centre):
    """Test that submitting the form works correctly."""
    department_leader.save()
    project.save()
    cost_centre.save()

    data = REFUND_DICT.copy()
    data["receipt_0_picture"] = open(os.path.join(TEST_DATA, "receipt_0.jpg"), "rb")
    data["receipt_0_amount"] = 29.99
    data["department_leader"] = department_leader.id
    data["project"] = project.id
    data["cost_centre"] = cost_centre.id

    response = client.post("/refund/new/", data=data, follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])

    filter_parameters = REFUND_DICT.copy()
    filter_parameters.pop("date_submitted")
    refunds = Refund.objects.filter(department_leader=department_leader, cost_centre=cost_centre,
                                    project=project, refund_type="cash",
                                    bank_account_owner="Mr Smith")

    assert len(refunds) == 1
    refund = refunds[0]
    assert refund.receipt_0_picture.name == "receipt_0.jpg"
    assert os.path.exists(refund.receipt_0_picture.path)

    assert "Your request has been successfully created." in str(response.content)

    data["receipt_0_picture"].close()
    TEMP_DIR.cleanup()
