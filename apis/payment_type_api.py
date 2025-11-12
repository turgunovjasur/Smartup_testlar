from apis.base_api import BaseAPI

class PaymentTypeAPI(BaseAPI):
    # ------------------------------------------------------------------------------------------------------------------

    def attach_payment_type(self, body):
        return self._post("/b/anor/mkr/payment_type_list+attach$attach", body)
    # ------------------------------------------------------------------------------------------------------------------

    def attach_payment_type_to_room(self, body):
        return self._post("/b/anor/mrf/room_attachment$attach_payment_type", body)

    # ------------------------------------------------------------------------------------------------------------------
