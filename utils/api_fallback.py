import json
import time
from datetime import datetime
from pathlib import Path
from utils.logger import configure_logging


class APIFallbackManager:
    """UI test fail bo'lganda API test bilan integratsiya."""

    def __init__(self, state_file="test_state.json"):
        self.state_file = Path(state_file)
        self.logger = configure_logging("APIFallbackManager")

    # ==================================================================================================================
    # PUBLIC API
    # ==================================================================================================================

    def execute_api_fallback(self, ui_test_name, api_test_func, save_data, load_data, ui_attempts=3):
        """
        UI test fail bo'lganda API testni ishga tushirish.

        Returns:
        --------
        dict or None: API test natijasi yoki None
        """
        self._log_fallback_start(ui_test_name, api_test_func.__name__, ui_attempts)

        start_time = time.time()

        try:
            # API testni bajarish
            api_test_func(save_data=save_data, load_data=load_data)

            # Muvaffaqiyat
            duration = time.time() - start_time
            self._log_fallback_success(api_test_func.__name__, duration)
            self._update_state(ui_test_name, api_test_func.__name__, "PASSED", duration, ui_attempts)

            return {"status": "PASSED", "duration": duration, "api_test": api_test_func.__name__}

        except Exception as e:
            # Xatolik
            duration = time.time() - start_time
            self._log_fallback_failure(api_test_func.__name__, duration, str(e))
            self._update_state(ui_test_name, api_test_func.__name__, "FAILED", duration, ui_attempts, str(e))

            return None

    def get_fallback_summary(self):
        """API fallback statistikasini olish."""
        states = self._load_states()

        stats = {"total": 0, "passed": 0, "failed": 0}

        for state in states.values():
            if self._has_fallback(state):
                stats["total"] += 1
                if self._is_fallback_passed(state):
                    stats["passed"] += 1
                else:
                    stats["failed"] += 1

        return {
            "total_fallbacks": stats["total"],
            "passed_fallbacks": stats["passed"],
            "failed_fallbacks": stats["failed"],
            "success_rate": f"{(stats['passed'] / stats['total'] * 100):.1f}%" if stats["total"] > 0 else "0%"
        }

    def print_fallback_report(self):
        """API fallback hisobotini chop etish."""
        summary = self.get_fallback_summary()

        if summary["total_fallbacks"] == 0:
            print("ℹ️ Hech qanday API fallback bajarilmagan")
            return

        print(f"\n{'='*80}")
        print(f"📊 API FALLBACK HISOBOTI")
        print(f"{'='*80}")
        print(f"Jami fallbacklar:        {summary['total_fallbacks']}")
        print(f"✅ Muvaffaqiyatli:       {summary['passed_fallbacks']}")
        print(f"❌ Muvaffaqiyatsiz:      {summary['failed_fallbacks']}")
        print(f"📈 Success rate:         {summary['success_rate']}")
        print(f"{'='*80}\n")

    # ==================================================================================================================
    # STATE MANAGEMENT
    # ==================================================================================================================

    def _load_states(self):
        """JSON dan holatlarni yuklash."""
        if not self.state_file.exists():
            return {}

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_states(self, states):
        """Holatlarni JSON ga saqlash."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(states, f, indent=4, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"State saqlashda xatolik: {e}")

    def _update_state(self, ui_test_name, api_test_name, api_status, duration, ui_attempts, error=None):
        """State'ni yangilash."""
        states = self._load_states()

        # API fallback ma'lumotlari
        fallback_data = {
            "executed": True,
            "api_test": api_test_name,
            "api_status": api_status,
            "api_duration": duration,
            "api_error": error,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ui_attempts": ui_attempts
        }

        # Mavjud state'ni yangilash yoki yangi yaratish
        if ui_test_name in states:
            states[ui_test_name]["api_fallback"] = fallback_data
            states[ui_test_name]["status"] = self._get_final_status(api_status)
            states[ui_test_name]["final_status"] = "CONTINUED_WITH_API" if api_status == "PASSED" else "FAILED"
        else:
            states[ui_test_name] = {
                "status": self._get_final_status(api_status),
                "attempt": ui_attempts,
                "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": "UI test failed, API fallback executed",
                "duration": None,
                "api_fallback": fallback_data
            }

        self._save_states(states)
        self.logger.info(f"📝 State yangilandi: {ui_test_name}")

    # ==================================================================================================================
    # LOGGING
    # ==================================================================================================================

    def _log_fallback_start(self, ui_test_name, api_test_name, ui_attempts):
        """Fallback boshlangani haqida log."""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"🔄 API FALLBACK: {ui_test_name}")
        self.logger.info(f"{'='*80}")

        print(f"\n{'='*80}")
        print(f"🔄 API FALLBACK")
        print(f"{'='*80}")
        print(f"📋 UI Test: {ui_test_name}")
        print(f"❌ UI: FAILED ({ui_attempts}x)")
        print(f"🔧 API: {api_test_name}")
        print(f"⏳ Ishga tushmoqda...\n")

    def _log_fallback_success(self, api_test_name, duration):
        """Fallback muvaffaqiyati haqida log."""
        self.logger.info(f"✅ API PASSED ({duration:.2f}s)")

        print(f"✅ API: PASSED ({duration:.2f}s)")
        print(f"{'='*80}")
        print(f"📦 Ma'lumotlar saqlandi")
        print(f"🔄 Testlar davom etadi\n")

    def _log_fallback_failure(self, api_test_name, duration, error):
        """Fallback xatosi haqida log."""
        self.logger.error(f"❌ API FAILED: {error}")

        print(f"❌ API: FAILED ({duration:.2f}s)")
        print(f"{'='*80}")
        print(f"🛑 Backend muammosi\n")

    # ==================================================================================================================
    # HELPERS
    # ==================================================================================================================

    @staticmethod
    def _get_final_status(api_status):
        """Final status."""
        return "FAILED_WITH_API_FALLBACK_PASSED" if api_status == "PASSED" else "FAILED_WITH_API_FALLBACK_FAILED"

    @staticmethod
    def _has_fallback(state):
        """Fallback bormi?"""
        return "api_fallback" in state and state["api_fallback"].get("executed", False)

    @staticmethod
    def _is_fallback_passed(state):
        """Fallback passed?"""
        return state.get("api_fallback", {}).get("api_status") == "PASSED"


# ======================================================================================================================
# ALLURE (Optional)
# ======================================================================================================================

def attach_fallback_to_allure(api_test_name, api_status, duration, error=None):
    """Allure reportga ma'lumot qo'shish."""
    try:
        import allure
        info = f"API Fallback\n{'='*50}\nTest: {api_test_name}\nStatus: {api_status}\nDuration: {duration:.2f}s\n"
        if error:
            info += f"\nError: {error}\n"
        allure.attach(info, name="API Fallback", attachment_type=allure.attachment_type.TEXT)
    except ImportError:
        pass