from apis.base_api import BaseAPI

class SectorAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def save_sector(self, body):
        return self._post("/b/anor/mr/sector+add:save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def model_sector(self, body):
        return self._post("/b/anor/mr/sector_view:model", body)

    # ------------------------------------------------------------------------------------------------------------------
