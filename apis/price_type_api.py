from apis.base_api import BaseAPI

class PriceTypeAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def import_price_type(self, body):
        return self._post("/b/anor/api/v2/mkr/price_type$import", body)

    # ------------------------------------------------------------------------------------------------------------------

    def export_price_type(self, body):
        return self._post("/b/anor/api/v2/mkr/price_type$export", body)

    # ------------------------------------------------------------------------------------------------------------------

    def price_type_list(self, body):
        return self._post("/b/anor/mkr/price_type_list:table", body)

    # ------------------------------------------------------------------------------------------------------------------

    def save_price_type(self, body):
        return self._post("/b/anor/mkr/price_type+add:save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def edit_price_type(self, body):
        return self._post("/b/anor/mkr/price_type+edit:save", body)
    # ------------------------------------------------------------------------------------------------------------------