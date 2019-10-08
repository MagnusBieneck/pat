"""Module containing global fixtures for all types of tests."""
import pytest
from django.contrib.auth.models import User, Group
from django.test import Client
from refund.models import Project, CostCentre, Refund

REFUND_DICT = {
        "date_submitted": "2019-06-06",
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


@pytest.fixture
def department_leader():
    """Fixture returning a department leader."""
    return User(username="john_doe", first_name="John", last_name="Doe", is_staff=True)


@pytest.fixture
def project():
    """Fixture returning a project."""
    return Project(name="Marketing")


@pytest.fixture
def cost_centre():
    """Fixture returning a cost centre."""
    return CostCentre(name="General Expenses")


# pylint: disable=redefined-outer-name
@pytest.fixture
def refund(refund_dict, department_leader, project, cost_centre):
    """Returns a refund instance."""
    requester = User(username="requester", first_name="Re", last_name="Quester")
    requester.save()

    department_leader.save()
    project.save()
    cost_centre.save()

    refund = Refund(**refund_dict, user=requester, department_leader=department_leader,
                    project=project, cost_centre=cost_centre)

    return refund


@pytest.fixture
def client():
    """Return a Django test client."""
    return _CLIENT


def _login(client, staff=False, superuser=False):
    """Helper function to create a user and log in."""
    username = "John Doe"
    password = "123456"

    user = User.objects.create_user(username, password=password, is_staff=staff,
                                    is_superuser=superuser)
    user.save()

    assert client.login(username=username, password=password)

    return user


@pytest.fixture
def login(client):
    """Login as a user."""
    return _login(client)


@pytest.fixture
def login_staff(client):
    """Login as a staff member."""
    return _login(client, staff=True)


@pytest.fixture
def login_superuser(client):
    """Login as a superuser."""
    return _login(client, superuser=True)


@pytest.fixture
def groups():
    """Fixture creating all groups that exist by default."""
    department_leaders = Group(id=1, name="Department Leader")
    department_leaders.save()

    return [department_leaders]
