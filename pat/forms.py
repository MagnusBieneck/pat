"""Module containing generic forms suitable for the entire project."""
from django.forms import ModelChoiceField


class UserChoiceField(ModelChoiceField):
    """Custom field that uses first name and last name as label instead of username."""

    def label_from_instance(self, obj):
        """Return first and last name as label."""
        return "{} {}".format(obj.first_name, obj.last_name)
