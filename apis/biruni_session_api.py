from apis.base_api import BaseAPI

class BiruniSessionAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def biruni_session(self, body):
        return self._post("/b/biruni/m:session", body)

    # ------------------------------------------------------------------------------------------------------------------
