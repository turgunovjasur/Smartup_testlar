from apis.base_api import BaseAPI

class FilialAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def import_filial(self, body):
        return self._post("/b/anor/mr/filial+add$save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def export_filial(self, body):
        return self._post("/b/anor/mr/filial_view:model", body)

    # ------------------------------------------------------------------------------------------------------------------
