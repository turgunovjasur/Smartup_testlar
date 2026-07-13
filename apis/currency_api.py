from apis.base_api import BaseAPI


class CurrencyAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def list_currencies(self, body):
        return self._post("/b/anor/mr/filial+add:currencies", body)

    # ------------------------------------------------------------------------------------------------------------------
