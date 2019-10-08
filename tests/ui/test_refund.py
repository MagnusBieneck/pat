"""Module containing UI tests for the refund app."""
import os
import tempfile
import pytest

from django.conf import settings
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.support.select import Select

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "integration", "refund",
                         "testdata", "test_refund_form")
TEMP_DIR = tempfile.TemporaryDirectory()
settings.MEDIA_ROOT = TEMP_DIR.name

"""
Caution: To simplify the creation of tests, the test cases in this module are allowed to depend on
each other. E.g., one test case might insert data that is later checked in a subsequent test case.
Therefore, be very careful when removing or reordering test cases!

Concerning the execution of this module: Do not execute the test methods in parallel!
"""


def test_refund_form_javascript(driver_standard):
    """Test that all the JavaScript in the form works correctly."""
    driver = driver_standard
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


def test_refund_form_submit(driver_standard):
    """Test that the refund form works correctly.

    The fields are filled out one after another. After each field, respectively, the submit button
    is hit to check the validation routine.
    """
    def check_error(element_id):
        """Asserts that the given element has an error."""
        assert (driver.find_element_by_id(f"error_1_{element_id}")
                .find_element_by_tag_name("strong").text) == "This field is required."

    driver = driver_standard
    driver.get("http://localhost:8000/refund/new/")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_refund_type")
    Select(driver.find_element_by_id("id_refund_type")).select_by_value("bank_account")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_department_leader")
    Select(driver.find_element_by_id("id_department_leader")).select_by_value("2")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_cost_centre")
    Select(driver.find_element_by_id("id_cost_centre")).select_by_value("1")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_project")
    Select(driver.find_element_by_id("id_project")).select_by_value("1")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_bank_account_owner")
    driver.find_element_by_id("id_bank_account_owner").send_keys("My Name")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_bank_account_iban")
    driver.find_element_by_id("id_bank_account_iban").send_keys("abc")

    driver.find_element_by_id("btn-submit").click()
    assert (driver.find_element_by_id("error_1_id_bank_account_iban")
            .find_element_by_tag_name("strong").text) == "A valid IBAN is required."
    driver.find_element_by_id("id_bank_account_iban").clear()
    driver.find_element_by_id("id_bank_account_iban").send_keys("DE02120300000000202051")

    driver.find_element_by_id("btn-submit").click()
    check_error("id_bank_account_bic")
    driver.find_element_by_id("id_bank_account_bic").send_keys("def")

    driver.find_element_by_id("btn-submit").click()
    assert (driver.find_element_by_id("error_1_id_bank_account_bic")
            .find_element_by_tag_name("strong").text) == "A valid BIC is required."
    driver.find_element_by_id("id_bank_account_bic").clear()
    driver.find_element_by_id("id_bank_account_bic").send_keys("BYLADEM1001")

    driver.find_element_by_id("btn-submit").click()
    assert (driver.find_element_by_id("error_1_id_receipt_0_picture")
            .find_element_by_tag_name("strong").text) == "At least one receipt is required."
    driver.find_element_by_id("id_receipt_0_amount").clear()
    driver.find_element_by_id("id_receipt_0_amount").send_keys("29.99")

    driver.find_element_by_id("btn-submit").click()
    assert (driver.find_element_by_id("error_1_id_receipt_0_amount")
            .find_element_by_tag_name("strong").text) == "The receipt for this amount is required."
    driver.find_element_by_id("id_receipt_0_picture").send_keys(
        os.path.join(TEST_DATA, "receipt_0.jpg"))

    driver.find_element_by_id("btn-submit").click()

    alert = driver.find_element_by_id("div-alert")
    assert "alert-success" in alert.get_attribute("class")
    assert alert.text == "Your request has been successfully created."


def test_refund_index(driver_standard):
    """Test that the form overview works correctly for standard users."""
    driver = driver_standard
    driver.get("http://localhost:8000/refund")

    assert driver.find_element_by_id("th_project").text == "Project"
    assert driver.find_element_by_id("th_department_leader").text == "Department Leader"
    assert driver.find_element_by_id("th_cost_centre").text == "Cost Centre"
    assert driver.find_element_by_id("th_total_amount").text == "Total Amount"
    with pytest.raises(NoSuchElementException):
        driver.find_element_by_id("th_requester")

    assert driver.find_elements_by_class_name("td-project")[-1].text == "My project"
    assert driver.find_elements_by_class_name("td-department-leader")[-1].text == \
        "tester-staff"
    assert driver.find_elements_by_class_name("td-cost-centre")[-1].text == "My cost centre"
    assert driver.find_elements_by_class_name("td-total-amount")[-1].text == "29.99 €"
    assert driver.find_elements_by_class_name("td-requester") == []


def test_refund_index_staff_unapproved(driver_staff):
    """Test that the form overview works correctly for staff users with unapproved request."""
    driver = driver_staff
    driver.get("http://localhost:8000/refund")

    assert driver.find_element_by_id("th_requester").text == "Requester"

    assert driver.find_elements_by_class_name("td-requester")[0].text == "Standard Tester"
    assert (driver.find_elements_by_class_name("td-approved")[0]
            .find_element_by_tag_name("span").text) == "Pending"
    assert (driver.find_elements_by_class_name("td-processed")[0]
            .find_element_by_tag_name("span").text) == "Pending"


def test_refund_form_approve(driver_staff):
    """Test that the form approval works correctly for staff users."""
    driver = driver_staff
    driver.get("http://localhost:8000/refund")

    # In overview page, click on the 'Edit' button
    (driver.find_elements_by_class_name("td-action")[0]
     .find_element_by_class_name("btn-edit").click())

    # In edit page, click on the 'Approve' button
    driver.find_element_by_id("a-approve").click()

    alert = driver.find_element_by_id("div-alert")
    assert "alert-success" in alert.get_attribute("class")
    assert alert.text == "The request has been successfully approved."


def test_refund_form_process(driver_superuser):
    """Test that the form processing works correctly for super users."""
    driver = driver_superuser
    driver.get("http://localhost:8000/refund")

    # In overview page, click on the 'Edit' button
    (driver.find_elements_by_class_name("td-action")[0]
     .find_element_by_class_name("btn-edit").click())

    # In edit page, click on the 'Process' button
    driver.find_element_by_id("a-process").click()

    alert = driver.find_element_by_id("div-alert")
    assert "alert-success" in alert.get_attribute("class")
    assert alert.text == "The request has been successfully processed."
