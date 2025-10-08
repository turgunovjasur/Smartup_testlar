from apis.base_api import BaseAPI

class NaturalPersonAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def import_natural_person(self, body):
        return self._post("/b/anor/mxsx/mr/natural_person$import", body)

    # ------------------------------------------------------------------------------------------------------------------

    def export_natural_person(self, body):
        return self._post("/b/anor/mxsx/mr/natural_person$export", body)

    # ------------------------------------------------------------------------------------------------------------------
