from autotest.biruni.modal_content.modal_content import ModalContent
from autotest.core.md.base_page import BasePage

# ----------------------------------------------------------------------------------------------------------------------

def get_biruni_confirm_flow(driver, **kwargs):
    modal = ModalContent(driver)
    base_page = BasePage(driver)

    result = {}

    if kwargs.get("is_visible"):
        modal.is_visible_biruni_confirm()
        base_page.logger.info(f"biruni_confirm: -> [visible=True]")
        result["is_visible"] = True

    if kwargs.get("get_body"):
        text = modal.get_biruni_confirm()
        base_page.logger.info(f"biruni_confirm: -> [get_body=True] -> text=[{text}]")
        result["get_body"] = text

    button_state = kwargs.get("button_state")
    if button_state:
        modal.click_biruni_confirm_button(button_state)
        base_page.logger.info(f"biruni_confirm: -> [button_state=True]")

    if result:
        return result

    base_page.logger.info("biruni_confirm: -> [result=None]")
    return None

# ----------------------------------------------------------------------------------------------------------------------

def get_biruni_alert_flow(driver, **kwargs):
    modal = ModalContent(driver)
    base_page = BasePage(driver)

    result = {}

    if kwargs.get("is_visible"):
        modal.is_visible_biruni_alert()
        base_page.logger.info(f"biruni_alert: -> [visible=True]")
        result["is_visible"] = True

    if kwargs.get("get_body"):
        text = modal.get_biruni_alert()
        base_page.logger.info(f"biruni_alert: -> [get_body=True] -> text=[{text}]")
        result["get_body"] = text

    if kwargs.get("close"):
        modal.click_biruni_alert_close_button()
        base_page.logger.info(f"biruni_alert: -> [close=True]")

    if result:
        return result

    base_page.logger.info("biruni_alert: -> [result=None]")
    return None
# ----------------------------------------------------------------------------------------------------------------------

def get_error_massage_flow(driver, error_massage_name):
    base_page = BasePage(driver)
    modal = ModalContent(driver)
    error_message = modal.error_massage()
    if error_message == error_massage_name:
        base_page.logger.info("Error message validated successfully")
        modal.click_error_close_button()
        return True
    else:
        base_page.logger.error(f'Error: Expected "{error_massage_name}", got "{error_message}"')
        base_page.take_screenshot(f"order_error_massage")
        raise AssertionError(f"Expected error message: '{error_massage_name}', got: '{error_message}'")

# ----------------------------------------------------------------------------------------------------------------------
