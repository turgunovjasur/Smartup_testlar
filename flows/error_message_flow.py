from autotest.biruni.error_message.error_message import ErrorMessage
from autotest.core.md.base_page import BasePage

# ----------------------------------------------------------------------------------------------------------------------
def get_error_massage(driver, error_massage_name):
    base_page = BasePage(driver)
    error_msg = ErrorMessage(driver)
    error_message = error_msg.error_massage()
    if error_message == error_massage_name:
        base_page.logger.info("Error message validated successfully")
        error_msg.click_error_close_button()
        return True
    else:
        base_page.logger.error(f'Error: Expected "{error_massage_name}", got "{error_message}"')
        base_page.take_screenshot(f"order_error_massage_{error_message.lower()}")
        raise AssertionError(f"Expected error message: '{error_massage_name}', got: '{error_message}'")
# ----------------------------------------------------------------------------------------------------------------------
