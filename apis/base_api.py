import json
import time
import allure
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry
from utils.env_reader import get_env
from utils.logger import get_test_name, configure_logging
from apis.response_utils import detect_response_type, pretty_body


class BaseAPI:
    # ==================================================================================================================

    def __init__(self, load_data,  **kwargs):
        self.base_url = get_env("URL")
        self.session = requests.Session()
        self.test_name = get_test_name()
        self.logger = configure_logging(self.test_name)

        headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "project_code": "trade",
        }

        filial_id = kwargs.get("filial_id") or load_data("api/filial_id")
        if filial_id:
            headers["filial_id"] = filial_id

        auth_profile = kwargs.get("auth_profile")
        if auth_profile == "admin":
            username = f"admin@{get_env('CODE_INPUT')}"
            password = get_env("PASSWORD_COMPANY")
        elif auth_profile == "user":
            username = f'api_test-{load_data("api/code")}@{get_env("CODE_INPUT")}'
            password = get_env("PASSWORD_USER")
        elif auth_profile:
            raise ValueError(f"Noma'lum auth_profile: {auth_profile}")
        else:
            username = password = None

        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)

        self.session.headers.update(headers)

        # Retry (agar vaqtinchalik xato bo‘lsa, avtomatik qayta urinish)
        retry_strategy = Retry(
            total=5,
            connect=3,
            read=3,
            status=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504, 429],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            respect_retry_after_header=True,
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,
            pool_maxsize=20,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    # ==================================================================================================================

    def log_api(self, resp, t_network, t_total, data=None):
        """
        Oddiy muvaffaqiyatli log yozish:
            - status, vaqt, hajm, qisqa javobni log qiladi.
        """
        size = len(resp.content or b"")
        self.logger.info(
            f"network={t_network:.2f}s | total={t_total:.2f}s "
            f"| size={size}B | status={resp.status_code}"
        )

        if data is not None:
            try:
                short = json.dumps(data, ensure_ascii=False)[:2000]
            except Exception:
                short = str(data)[:2000]
            self.logger.debug(f"Javob (short): {short}...")

    # ==================================================================================================================

    def log_error(self, resp, t_network, t_total, body=None):
        """
        Serverdan xato javob kelsa, bu funksiya:
            - status, vaqt, request body va server javobini log qiladi.
            - Allure’ga ham attach qiladi.
        """
        self.logger.error(
            f"API Error: status={resp.status_code} "
            f"| network={t_network:.2f}s | total={t_total:.2f}s"
        )

        if body is not None:
            try:
                short_body = json.dumps(body, ensure_ascii=False, indent=2)
            except Exception:
                short_body = str(body)
            self.logger.error(f"Request body:\n{short_body}")

        raw_response = pretty_body(resp)
        self.logger.error(f"Server response:\n{raw_response[:2000]}")

        allure.attach(
            raw_response,
            name=f"Response (status={resp.status_code})",
            attachment_type=allure.attachment_type.TEXT
        )

        if body is not None:
            allure.attach(
                json.dumps(body, ensure_ascii=False, indent=2),
                name=f"Request Body",
                attachment_type=allure.attachment_type.JSON
            )

    # ==================================================================================================================

    def handle_response(self, resp, t_network, t_total, body=None, expect_status=200, allow_empty_response=False):
        """
        Bu funksiya – barchasini boshqaradi.
            - Agar status `expect_status` bo'lsa → log_api()
            - Aks holda → log_error() va AssertionError chiqaradi.
            - allow_empty_response=True bo'lsa, bo'sh javobni qabul qiladi
        """
        if resp.status_code == expect_status:
            if not resp.content or len(resp.content) == 0:
                if allow_empty_response:
                    self.log_api(resp, t_network, t_total, data=None)
                    return None
                else:
                    self.logger.error(f"Empty response!")
                    self.log_error(resp, t_network, t_total, body)
                    raise AssertionError("Empty response!")
            try:
                data = resp.json()
                self.log_api(resp, t_network, t_total, data=data)
                return data
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON parse xatosi: {e}")
                self.log_error(resp, t_network, t_total, body)
                raise AssertionError(f"Invalid JSON response: {resp.text[:500]}")

        raise AssertionError(
            f"\nAPI failed:"
            f"\nExpected: {expect_status}, Got: {resp.status_code}"
            f"\nURL: {resp.url}"
            f"\nNetwork: {t_network:.2f}s | Total: {t_total:.2f}s"
            f"\nRequest body: {json.dumps(body, ensure_ascii=False) if body else '<empty>'}"
            f"\nResponse ({detect_response_type(resp)}):\n{pretty_body(resp)[:2000]}"
        )

    # ==================================================================================================================

    def _post(self, path, body, timeout=(3.05, 60)):
        """
        Serverga POST so‘rov yuboradi:
            - vaqtni o‘lchaydi
            - javob, t_network, t_total qiymatlarini qaytaradi
        """
        url = f"{self.base_url}{path}"
        t0 = time.perf_counter()

        resp = self.session.post(url, json=body, timeout=timeout)
        t_total = time.perf_counter() - t0
        t_network = resp.elapsed.total_seconds()

        return resp, t_network, t_total

    # ==================================================================================================================
