from apis.base_api import BaseAPI

class RoleAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def role_edit(self, body):
        return self._post("/b/trade/tr/role+edit:save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def role_view(self, body):
        return self._post("/b/biruni/md/role_view:model", body)

    # ------------------------------------------------------------------------------------------------------------------

    def access_generate_all(self, body):
        return self._post("/b/biruni/md/role_form_list$access_generate_all", body)

    # ------------------------------------------------------------------------------------------------------------------
