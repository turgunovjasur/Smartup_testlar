import pytest
import os
from datetime import datetime
from apis.price_tag_excel_api import PriceTagExcelAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(37)
def test_price_tag_excel_download(save_data, load_data):
    """Price Tag Excel yuklab olish - bitta mahsulot"""
    api = PriceTagExcelAPI(load_data, auth_profile="user")

    price_type_id = load_data("api/price_type_uzb_id")
    product_id = load_data("api/product_id")

    params = {
        "price_type_id": price_type_id,
        "product_ids": [product_id],
        "card_codes": [" "]
    }

    resp, t_network, t_total = api.download_excel(params)

    # Status code tekshirish
    assert resp.status_code == 200, f"Status code: {resp.status_code}"

    # Content type tekshirish
    content_type = resp.headers.get("Content-Type", "")
    assert "excel" in content_type.lower() or "spreadsheet" in content_type.lower() or "octet-stream" in content_type.lower(), \
        f"Noto'g'ri content type: {content_type}"

    # File hajmi tekshirish
    file_size = len(resp.content)
    assert file_size > 0, "Excel file bo'sh"

    # File ni saqlash (optional)
    os.makedirs("downloads", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"downloads/price_tag_{timestamp}.xlsx"

    with open(filename, 'wb') as f:
        f.write(resp.content)

    save_data("api/price_tag_excel_file", filename)

    api.logger.info(f"✅ Excel yuklab olindi: {filename} ({file_size} bytes)")
    api.logger.info(f"⏱️  Network: {t_network:.2f}s, Total: {t_total:.2f}s")

# ----------------------------------------------------------------------------------------------------------------------