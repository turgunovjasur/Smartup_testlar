from apis.base_api import BaseAPI


class PriceTagExcelAPI(BaseAPI):
    """Price Tag Excel yuklab olish API"""
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, load_data, **kwargs):
        super().__init__(load_data, **kwargs)
        self.load_data = load_data

    # ------------------------------------------------------------------------------------------------------------------

    def download_excel(self, params):
        url = f"{self.base_url}/b/anor/mkr/price_tag:run"

        # Default qiymatlar
        if "card_codes" not in params:
            params["card_codes"] = [" "] * len(params.get("product_ids", []))

        if "date" not in params:
            from datetime import datetime
            params["date"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Query parameters
        query_params = {
            "price_type_id": params["price_type_id"],
            "rt": "xlsx",
            "date": params["date"],
            "product_ids": params["product_ids"],
            "card_codes": params["card_codes"],
            "-project_code": "trade",
            "-project_hash": "01",
            "-filial_id": params.get("filial_id") or self.load_data("api/filial_id"),
            "-user_id": params.get("user_id") or self.load_data("api/user_id"),
            "-lang_code": "ru"
        }

        return self.get(url, params=query_params)

    # ------------------------------------------------------------------------------------------------------------------