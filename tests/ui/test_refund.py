"""Module containing UI tests for the refund app."""
from selenium.webdriver.support.select import Select


def test_refund_form(driver):
    """Test that the refund form works correctly."""
    driver.get("http://localhost:8000/refund/new/")

    form_content = [
        ("department_leader", "My department leader"),
        ("account", "My account"),
        ("cost_centre", "My cost centre"),
        ("project", "My project"),
        ("bank_account_owner", "My Name"),
        ("bank_account_iban", "DE1234567890"),
        ("bank_account_bic", "MYBIC1FOO")
    ]

    for field, content in form_content:
        field = driver.find_element_by_id("id_{}".format(field))
        field.send_keys(content)

    Select(driver.find_element_by_id("id_refund_type")).select_by_value("cash")

    driver.find_element_by_id("btn-submit").click()

    alert = driver.find_element_by_id("div-alert")
    assert "alert-success" in alert.get_attribute("class")
    assert alert.text == "Your request has been successfully created."
