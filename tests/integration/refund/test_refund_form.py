"""Module containing integration tests for the refund form."""
from django.test import TransactionTestCase, Client
from refund.models import Refund
from tests.conftest import REFUND_DICT


class TestRefundForm(TransactionTestCase):
    """Wrapper class for test cases."""

    def test_form(self):
        """Test that the form appears correctly."""
        client = Client()
        response = client.get("/")

        assert response.status_code == 200

        for field, length, required in [
                ("department_leader", 128, True),
                ("account", 128, True),
                ("cost_centre", 128, True),
                ("project", 256, False),
                ("bank_account_owner", 128, False),
                ("bank_account_iban", 128, False),
                ("bank_account_bic", 128, False)
            ]:
            html_element = '<input type="text" name="{element}" maxlength="{length}" {required} ' \
                           'class="textinput textInput form-control" id="id_{element}">' \
                .format(element=field, length=length,
                        required=" required" if required else "")
            self.assertInHTML(html_element, str(response.content))

    # pylint: disable=no-self-use, no-member
    def test_submit(self):
        """Test that submitting the form works correctly."""
        client = Client()
        response = client.post("/", data=REFUND_DICT, follow=True)

        assert response.status_code == 200

        filter_parameters = REFUND_DICT.copy()
        filter_parameters.pop("date_submitted")
        refunds = Refund.objects.filter(department_leader="John Doe", account="Dunno",
                                        cost_centre="General Expenses", project="Conference",
                                        refund_type="cash", bank_account_owner="Mr Smith")
        assert len(refunds) == 1
