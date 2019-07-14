"""Module containing tests for the PAT models."""
from django.contrib.auth.models import User
import pytest

from pat.models import PATUser


@pytest.mark.django_db
def test_get_department_leader(groups):
    """Test that the list of department leaders is returned correctly."""
    department_leaders = groups[0]

    dp_one = User.objects.create(username="dp_one")
    dp_one.groups.add(department_leaders)
    dp_two = User.objects.create(username="dp_two")
    dp_two.groups.add(department_leaders)
    other_user = User.objects.create(username="other")

    assert dp_one in PATUser.get_department_leader()
    assert dp_two in PATUser.get_department_leader()
    assert other_user not in PATUser.get_department_leader()
