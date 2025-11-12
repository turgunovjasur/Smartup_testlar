from apis.base_api import BaseAPI

class InventoryAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def save_inventory(self, body):
        return self._post("/b/anor/mr/product/inventory+add$save", body)
    # ------------------------------------------------------------------------------------------------------------------

    def model_inventory(self, body):
        return self._post("/b/anor/mr/product/inventory_view:model", body)

    # ------------------------------------------------------------------------------------------------------------------
