from apis.base_api import BaseAPI

class LegalPersonAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def import_legal_person(self, body):
        return self._post("/b/anor/mxsx/mr/legal_person$import", body)

    # ------------------------------------------------------------------------------------------------------------------

    def export_legal_person(self, body):
        return self._post("/b/anor/mxsx/mr/legal_person$export", body)

    # ------------------------------------------------------------------------------------------------------------------
