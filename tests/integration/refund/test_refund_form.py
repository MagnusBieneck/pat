"""Module containing integration tests for the refund form."""
from datetime import datetime, timezone
import os
import tempfile
import pytest

from bs4 import BeautifulSoup
from django.contrib.auth.models import User

from pat import settings
from refund.models import Refund, Project, CostCentre
from tests.conftest import REFUND_DICT

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata", "test_refund_form")


@pytest.mark.django_db
def test_form(login, client):  # pylint: disable=unused-argument
    """Test that the form appears correctly."""
    response = client.get("/refund/new/")

    assert response.status_code == 200
    assert any([template.name == "refund/request_form.html" for template in response.templates])


# pylint: disable=no-member, unused-argument
@pytest.mark.django_db
def test_submit(login, client, department_leader, project, cost_centre, mocker):
    """Test that submitting the form works correctly."""
    department_leader.save()
    project.save()
    cost_centre.save()

    with tempfile.TemporaryDirectory() as temp_dir:
        print("Submit", temp_dir)
        mocker.patch.object(settings, "MEDIA_ROOT", temp_dir)
        assert settings.MEDIA_ROOT == temp_dir

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
        refunds = Refund.objects.filter(department_leader=department_leader,
                                        cost_centre=cost_centre,
                                        project=project, refund_type="cash",
                                        bank_account_owner="Mr Smith")

        assert len(refunds) == 1
        refund = refunds[0]
        assert os.path.exists(refund.receipt_0_picture.path)

        assert "Your request has been successfully created." in str(response.content)

        data["receipt_0_picture"].close()


def _create_request(user, department_leader, approved=False, processed=False):
    """Helper function that creates a request."""
    department_leader.save()
    project = Project(name="Marketing")
    project.save()
    cost_centre = CostCentre(name="General Expenses")
    cost_centre.save()

    data = REFUND_DICT.copy()
    data["receipt_0_amount"] = 29.99
    data["department_leader"] = department_leader
    data["user"] = user
    data["project"] = project
    data["cost_centre"] = cost_centre
    data["approved"] = datetime.now(tz=timezone.utc) if approved else None
    data["processed"] = datetime.now(tz=timezone.utc) if processed else None

    refund = Refund(**data)
    refund.save()

    return Refund.objects.first()


@pytest.mark.django_db
def test_edit(login_staff, client):
    """Test that editing the form works correctly."""
    refund = _create_request(user=login_staff, department_leader=login_staff)
    refund_id = refund.id

    response = client.get(f"/refund/edit/{refund_id}", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/request_form.html" for template in response.templates])


@pytest.mark.django_db
def test_approve(login_staff, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login_staff, department_leader=login_staff)
    refund_id = refund.id
    assert not refund.is_approved

    response = client.get(f"/refund/approve/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert "The request has been successfully approved." in str(response.content)

    assert Refund.objects.first().is_approved


@pytest.mark.django_db
def test_approve_already_approved(login_staff, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login_staff, department_leader=login_staff, approved=True)
    refund_id = refund.id
    assert refund.is_approved

    response = client.get(f"/refund/approve/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert "This request has already been approved." in str(response.content)


@pytest.mark.django_db
def test_approve_no_staff(login, department_leader, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login, department_leader=department_leader)
    refund_id = refund.id
    assert not refund.is_approved

    response = client.get(f"/refund/approve/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert ("You cannot approve any requests as you are no department leader."
            in str(response.content))

    assert not Refund.objects.first().is_approved


@pytest.mark.django_db
def test_approve_not_own_department(login_staff, department_leader, client):
    """Test that approving the form works correctly."""
    user = User.objects.create_user("foo", password="bar")
    user.save()

    refund = _create_request(user=user, department_leader=department_leader)
    refund_id = refund.id
    assert not refund.is_approved

    response = client.get(f"/refund/approve/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert ("You can only approve requests within your own department."
            in str(response.content))

    assert not Refund.objects.first().is_approved


@pytest.mark.django_db
def test_process(login_superuser, department_leader, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login_superuser, department_leader=department_leader,
                             approved=True)
    refund_id = refund.id
    assert not refund.is_processed

    response = client.get(f"/refund/process/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert "The request has been successfully processed." in str(response.content)

    assert Refund.objects.first().is_processed


@pytest.mark.django_db
def test_process_already_processed(login_superuser, department_leader, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login_superuser, department_leader=department_leader,
                             approved=True, processed=True)
    refund_id = refund.id
    assert refund.is_processed

    response = client.get(f"/refund/process/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert "This request has already been processed." in str(response.content)

    assert Refund.objects.first().is_processed


@pytest.mark.django_db
def test_process_not_approved(login_superuser, department_leader, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login_superuser, department_leader=department_leader,
                             approved=False)
    refund_id = refund.id
    assert not refund.is_approved
    assert not refund.is_processed

    response = client.get(f"/refund/process/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert "This request must be approved before it can be processed." in str(response.content)

    assert not Refund.objects.first().is_processed


@pytest.mark.django_db
def test_process_no_superuser(login_staff, department_leader, client):
    """Test that approving the form works correctly."""
    refund = _create_request(user=login_staff, department_leader=department_leader,
                             approved=True)
    refund_id = refund.id
    assert not refund.is_processed

    response = client.get(f"/refund/process/{refund_id}/", follow=True)

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
    assert "You cannot approve any requests as you are no finance leader." in str(response.content)

    assert not Refund.objects.first().is_processed


@pytest.mark.django_db
@pytest.mark.parametrize("existing_requests,expected_content", [
    ([("foo", "ABCDEFG", "MB1234")],
     ("foo", "ABCDEFG", "MB1234")),
])  # pylint: disable=too-many-arguments
def test_account_prefill(login, existing_requests, expected_content, project, cost_centre, client):
    """Test that pre-filling bank account information works correctly."""
    cost_centre.save()
    project.save()

    for owner, iban, bic in existing_requests:
        data = REFUND_DICT.copy()
        data["receipt_0_amount"] = 29.99
        data["department_leader"] = login
        data["user"] = login
        data["project"] = project
        data["cost_centre"] = cost_centre
        data["refund_type"] = "bank_account"
        data["bank_account_owner"] = owner
        data["bank_account_iban"] = iban
        data["bank_account_bic"] = bic
        refund = Refund(**data)
        refund.save()

    response = client.get("/refund/new/", follow=True)
    html = BeautifulSoup(response.content)

    owner, iban, bic = expected_content
    assert html.find("input", id="id_bank_account_owner").get("value") == owner
    assert html.find("input", id="id_bank_account_iban").get("value") == iban
    assert html.find("input", id="id_bank_account_bic").get("value") == bic
