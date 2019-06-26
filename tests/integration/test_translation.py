"""Module containing tests for the translation files."""
import os
import pytest


@pytest.mark.parametrize("language_code", ['de'])
def test_untranslated_parts(language_code):
    """Test that there are no untranslated parts in the *.po files."""
    locale_dir = "locale/{}/LC_MESSAGES".format(language_code)

    for file_name in os.listdir(locale_dir):
        if file_name.endswith(".po"):

            with open("{}/{}".format(locale_dir, file_name)) as file:

                # THere is always one occurrence of an empty msgstr in the beginning of a .po file.
                assert file.read().count('msgstr ""') == 2
