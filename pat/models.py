"""Module containing extensions for core models."""
from django.contrib.auth.models import Group


class PATUser:                                              # pylint: disable=too-few-public-methods
    """Extends Django User class."""

    @staticmethod
    def get_department_leader():
        """Returns all department leaders.

        A department leader is a user that belongs to a certain group.

        Returns:
            list[django.contrib.auth.models.User]: The department leaders.
        """
        return Group.objects.get(name="Department Leader").user_set.all()
