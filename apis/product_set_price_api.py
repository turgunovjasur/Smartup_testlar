from apis.base_api import BaseAPI

class ProductSetPriceAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def save_product_set_price(self, body):
        return self._post("/b/anor/mr/product/product_set_price$save", body)
    # ------------------------------------------------------------------------------------------------------------------

    def model_product_set_price(self, body):
        return self._post("/b/anor/mr/product/product_set_price:model", body)

    # ------------------------------------------------------------------------------------------------------------------
