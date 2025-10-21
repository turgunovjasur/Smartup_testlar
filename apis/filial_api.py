from apis.base_api import BaseAPI

class FilialAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def filial_save(self, body):
        return self._post("/b/anor/mr/filial+add$save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def filial_model(self, body):
        return self._post("/b/anor/mr/filial_view:model", body)

    # ------------------------------------------------------------------------------------------------------------------
