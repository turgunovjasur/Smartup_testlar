from apis.base_api import BaseAPI

class UserAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def user_add(self, body):
        return self._post("/b/anor/mr/user+add:save", body)

    # ------------------------------------------------------------------------------------------------------------------

    def user_view(self, body):
        return self._post("/b/anor/mr/user_view:model", body)

    # ------------------------------------------------------------------------------------------------------------------

    def user_form_list(self, body):
        return self._post("/b/biruni/md/user_form_list:form_table", body)

    # ------------------------------------------------------------------------------------------------------------------

    def user_form_attach(self, body):
        return self._post("/b/biruni/md/user_form_list$attach", body)

    # ------------------------------------------------------------------------------------------------------------------
