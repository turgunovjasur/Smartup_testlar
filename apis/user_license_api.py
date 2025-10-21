from apis.base_api import BaseAPI

class UserLicenseAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def balance_info(self, body):
        return self._post("/b/biruni/kl/license_list:balance_info", body)
    # ------------------------------------------------------------------------------------------------------------------

    def purchase_info(self, body):
        return self._post("/b/biruni/kl/license_list:purchase_info", body)
    # ------------------------------------------------------------------------------------------------------------------

    def purchase_license(self, body):
        return self._post("/b/biruni/kl/license_list:purchase", body)
    # ------------------------------------------------------------------------------------------------------------------

    def license_list(self, body):
        return self._post("/b/biruni/kl/license_list:table_license", body)
    # ------------------------------------------------------------------------------------------------------------------

    def license_user_attach(self, body):
        return self._post("/b/biruni/kl/license_user_list$attach", body)

    # ------------------------------------------------------------------------------------------------------------------
