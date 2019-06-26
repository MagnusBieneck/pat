"""Module containing UI tests for the refund app."""
import pytest

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.select import Select


def test_refund_form_javascript(driver):
    """Test that all the JavaScript in the form works correctly."""
    driver.get("http://localhost:8000/refund/new/")

    # # Refund type checkbox # #
    for refund_type in ["cash", "amazon", "credit_card"]:
        with pytest.raises(ElementNotInteractableException):
            Select(driver.find_element_by_id("id_refund_type")).select_by_value(refund_type)
            driver.find_element_by_id("id_bank_account_owner").click()
            driver.find_element_by_id("id_bank_account_iban").click()
            driver.find_element_by_id("id_bank_account_bic").click()

    Select(driver.find_element_by_id("id_refund_type")).select_by_value("bank_account")
    assert driver.find_element_by_id("id_bank_account_owner")
    assert driver.find_element_by_id("id_bank_account_iban")
    assert driver.find_element_by_id("id_bank_account_bic")

    # # Total sum # #
    driver.find_element_by_id("id_receipt_0_amount").send_keys("12.34")
    driver.find_element_by_id("btn_show_next_receipt").click()
    driver.find_element_by_id("id_receipt_1_amount").send_keys("56.78")
    assert driver.find_element_by_id("span_amount_total").text == "69,12"


def test_refund_form_submit(driver):
    """Test that the refund form works correctly."""
    driver.get("http://localhost:8000/refund/new/")

    Select(driver.find_element_by_id("id_refund_type")).select_by_value("bank_account")
    driver.find_element_by_id("id_department_leader").send_keys("My department leader")
    driver.find_element_by_id("id_account").send_keys("My account")
    driver.find_element_by_id("id_cost_centre").send_keys("My cost centre")
    driver.find_element_by_id("id_project").send_keys("My project")
    driver.find_element_by_id("id_bank_account_owner").send_keys("My Name")
    driver.find_element_by_id("id_bank_account_iban").send_keys("DE1234567890")
    driver.find_element_by_id("id_bank_account_bic").send_keys("MYBIC1FOO")

    driver.find_element_by_id("btn-submit").click()

    alert = driver.find_element_by_id("div-alert")
    assert "alert-success" in alert.get_attribute("class")
    assert alert.text == "Your request has been successfully created."
