from apis.base_api import BaseAPI

class RobotAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def import_robot(self, body):
        return self._post("/b/anor/mrf/robot+add:save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def export_robot(self, body):
        return self._post("/b/anor/mrf/robot+add:model", body)

    # ------------------------------------------------------------------------------------------------------------------
