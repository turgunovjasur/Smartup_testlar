from autotest.biruni.modal_content.modal_content import ModalContent

# ----------------------------------------------------------------------------------------------------------------------
def get_modal_content_flow(driver, button_state):
    modal = ModalContent(driver)
    text = modal.get_modal_content()
    modal.click_modal_button(button_state)
    return text

# ----------------------------------------------------------------------------------------------------------------------
