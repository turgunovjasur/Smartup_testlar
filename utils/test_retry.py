import functools
import json
import time
from datetime import datetime
from pathlib import Path
from utils.driver_manager import cleanup_driver, create_driver
from utils.logger import configure_logging

# ======================================================================================================================
# Test State Manager
# ======================================================================================================================

class TestStateManager:
    """Test holatlarini boshqarish."""

    def __init__(self, state_file="test_state.json"):
        self.state_file = Path(state_file)
        self.states = self._load_states()

    # PUBLIC API =======================================================================================================

    def get_state(self, test_name):
        """Test holatini olish."""
        return self.states.get(test_name, {})

    def update_state(self, test_name, status, attempt=1, error=None, duration=None):
        """Test holatini yangilash."""
        self.states[test_name] = {
            "status": status,
            "attempt": attempt,
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(error) if error else None,
            "duration": duration
        }
        self._save_states()

    def is_passed(self, test_name):
        """Test passed yoki API fallback orqali davom etganmi?"""
        state = self.get_state(test_name)

        # 1. Oddiy passed
        if state.get("status") == "PASSED":
            return True

        # 2. API fallback passed
        if state.get("status") == "FAILED_WITH_API_FALLBACK_PASSED":
            if state.get("final_status") == "CONTINUED_WITH_API":
                return True

        return False

    def get_dependency_info(self, test_name):
        """Dependency haqida batafsil ma'lumot."""
        state = self.get_state(test_name)

        if not state:
            return self._dep_info(False, "NOT_RUN", False, False, "Hali ishga tushirilmagan")

        status = state.get("status")
        has_fb = "api_fallback" in state and state["api_fallback"].get("executed", False)
        fb_passed = has_fb and state["api_fallback"].get("api_status") == "PASSED"

        # Status bo'yicha ma'lumot
        if status == "PASSED":
            return self._dep_info(True, status, False, False, "UI test passed")

        elif status == "FAILED_WITH_API_FALLBACK_PASSED":
            if state.get("final_status") == "CONTINUED_WITH_API":
                api_name = state["api_fallback"]["api_test"]
                return self._dep_info(True, status, True, True, f"UI fail, API ({api_name}) passed")

        elif status == "FAILED_WITH_API_FALLBACK_FAILED":
            api_name = state["api_fallback"]["api_test"]
            return self._dep_info(False, status, True, False, f"UI va API ({api_name}) fail - backend muammosi")

        elif status == "FAILED":
            return self._dep_info(False, status, has_fb, fb_passed, "Test fail" + (", API yo'q" if not has_fb else ""))

        elif status == "SKIPPED":
            return self._dep_info(False, status, False, False, f"Skip: {state.get('error', 'Nomalum')}")

        return self._dep_info(False, status or "UNKNOWN", has_fb, fb_passed, f"Noma'lum: {status}")

    def reset_state(self, test_name):
        """Test holatini o'chirish."""
        if test_name in self.states:
            del self.states[test_name]
            self._save_states()

    def reset_all_states(self):
        """Barcha holatlarni tozalash."""
        self.states = {}
        self._save_states()

    # PRIVATE ==========================================================================================================

    def _load_states(self):
        """JSON dan yuklash."""
        if not self.state_file.exists():
            return {}
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_states(self):
        """JSON ga saqlash."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.states, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ State saqlash xatosi: {e}")

    @staticmethod
    def _dep_info(passed, status, has_api, api_passed, message):
        """Dependency info tuzish."""
        return {
            'passed': passed,
            'status': status,
            'has_api_fallback': has_api,
            'api_fallback_passed': api_passed,
            'message': message
        }


# ======================================================================================================================
# Retry Decorator
# ======================================================================================================================

def retry_on_failure(retry_count=3, retry_delay=5, dependencies=None):
    """
    Test retry va dependency check decorator.

    Faqat dependencies mavjud bo'lsa yoki retry_count > 1 bo'lsa ishlatiladi.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            test_name = func.__name__
            logger = configure_logging(test_name)
            state_manager = TestStateManager()

            # Driver va test_data ni topish
            driver, test_data = _get_fixtures(args, kwargs)
            if not driver or not test_data:
                raise ValueError(f"{test_name}: 'driver' va 'test_data' topilmadi")

            # Dependency tekshirish
            if dependencies:
                _check_dependencies(test_name, dependencies, state_manager)

            # Retry loop
            return _retry_loop(
                func, test_name, logger, state_manager,
                driver, test_data, args, kwargs,
                retry_count, retry_delay
            )

        return wrapper

    return decorator


# ======================================================================================================================
# Helper Functions
# ======================================================================================================================

def _get_fixtures(args, kwargs):
    """driver va test_data ni topish."""
    driver = kwargs.get('driver') or (args[0] if len(args) > 0 else None)
    test_data = kwargs.get('test_data') or (args[1] if len(args) > 1 else None)
    return driver, test_data


def _check_dependencies(test_name, dependencies, state_manager):
    """Dependency'larni tekshirish."""
    print(f"\n{'=' * 80}")
    print(f"🔍 DEPENDENCY CHECK: {test_name}")
    print(f"{'=' * 80}")

    failed_deps = []
    detailed_info = []

    for dep in dependencies:
        dep_info = state_manager.get_dependency_info(dep)

        _print_dep_info(dep, dep_info)

        if not dep_info['passed']:
            failed_deps.append(dep)
            detailed_info.append(f"{dep}: {dep_info['message']}")

    if failed_deps:
        _skip_test(test_name, failed_deps, detailed_info, state_manager)
    else:
        print(f"\n✅ Barcha dependency'lar OK!")
        print(f"{'=' * 80}\n")


def _print_dep_info(dep, info):
    """Dependency ma'lumotini chop etish."""
    print(f"\n📋 {dep}")
    print(f"   Status: {info['status']}")
    print(f"   Passed: {'✅' if info['passed'] else '❌'}")
    if info['has_api_fallback']:
        print(f"   API FB: {'✅' if info['api_fallback_passed'] else '❌'}")
    print(f"   Info: {info['message']}")


def _skip_test(test_name, failed_deps, detailed_info, state_manager):
    """Testni skip qilish."""
    print(f"\n{'=' * 80}")
    print(f"⭐️ {test_name} SKIP")
    print(f"{'=' * 80}")
    print(f"Sabab: Dependency'lar fail:\n")

    for info in detailed_info:
        print(f"   ❌ {info}")

    print(f"\n{'=' * 80}\n")

    msg = f"Dependencies fail: {failed_deps}"
    state_manager.update_state(test_name, "SKIPPED", error=msg)

    import pytest
    pytest.skip(msg)


def _retry_loop(func, test_name, logger, state_manager, driver, test_data, args, kwargs, retry_count, retry_delay):
    """Test retry loop."""
    last_exception = None
    current_driver = driver
    user_data_dir = None
    start_time = time.time()

    for attempt in range(1, retry_count + 1):
        # 2+ urinishda yangi driver
        if attempt > 1:
            logger.info(f"🔧 Yangi driver yaratilmoqda ({attempt})...")
            current_driver, user_data_dir, start_time = create_driver(test_name, test_data)
            args, kwargs = _update_driver(args, kwargs, current_driver)

        try:
            print(f"\n{'=' * 70}")
            print(f"🔄 {test_name} - Urinish {attempt}/{retry_count}")
            print(f"{'=' * 70}")

            # Test
            result = func(*args, **kwargs)

            # Passed
            duration = time.time() - start_time
            state_manager.update_state(test_name, "PASSED", attempt, duration=duration)

            print(f"\n✅ {test_name} PASSED ({duration:.2f}s)\n")

            if attempt > 1 and current_driver:
                cleanup_driver(current_driver, user_data_dir, logger, start_time, test_name)

            return result

        except Exception as e:
            last_exception = e
            duration = time.time() - start_time

            logger.error(f"❌ Urinish {attempt}/{retry_count} FAILED")

            # Driver yopish
            _cleanup_driver_safe(attempt, driver, current_driver, user_data_dir, logger, start_time, test_name)

            if attempt == retry_count:
                # Oxirgi urinish
                state_manager.update_state(test_name, "FAILED", attempt, str(e), duration)
                print(f"\n❌ {test_name} FAILED ({retry_count}x)\n")
                raise last_exception
            else:
                # Yana urinish
                print(f"\n⚠️ {test_name} FAILED ({attempt}/{retry_count})")
                print(f"⏳ {retry_delay}s kutish...\n")
                state_manager.update_state(test_name, "RETRY", attempt, str(e), duration)
                time.sleep(retry_delay)


def _update_driver(args, kwargs, new_driver):
    """Driver ni yangilash."""
    if 'driver' in kwargs:
        kwargs['driver'] = new_driver
    else:
        args_list = list(args)
        args_list[0] = new_driver
        args = tuple(args_list)
    return args, kwargs


def _cleanup_driver_safe(attempt, driver, current_driver, user_data_dir, logger, start_time, test_name):
    """Driverni xavfsiz yopish."""
    try:
        if attempt == 1:
            logger.info("🔒 Birinchi driver yopilmoqda...")
            driver.quit()
        else:
            logger.info("🔒 Yangi driver tozalanmoqda...")
            cleanup_driver(current_driver, user_data_dir, logger, start_time, test_name)
    except Exception as e:
        logger.warning(f"⚠️ Driver yopish xatosi: {e}")


# ======================================================================================================================
# Utility Functions
# ======================================================================================================================

def reset_test_state(test_name=None):
    """Test holatini o'chirish."""
    state_manager = TestStateManager()
    if test_name:
        state_manager.reset_state(test_name)
        print(f"✅ {test_name} holati o'chirildi")
    else:
        state_manager.reset_all_states()
        print(f"✅ Barcha holatlar o'chirildi")


def print_test_states():
    """Barcha test holatlarini ko'rsatish."""
    state_manager = TestStateManager()

    if not state_manager.states:
        print("Holatlar topilmadi")
        return

    print(f"\n{'=' * 80}")
    print(f"📋 TEST HOLATLARI")
    print(f"{'=' * 80}")

    for test_name, state in state_manager.states.items():
        emoji = {
            "PASSED": "✅",
            "FAILED": "❌",
            "FAILED_WITH_API_FALLBACK_PASSED": "🔄✅",
            "FAILED_WITH_API_FALLBACK_FAILED": "🔄❌",
            "SKIPPED": "⭐️",
            "RETRY": "🔄"
        }.get(state.get("status"), "❓")

        print(f"\n{emoji} {test_name}")
        print(f"Status: {state.get('status')}")
        print(f"Attempt: {state.get('attempt')}")

        if state.get('duration'):
            print(f"Duration: {state.get('duration'):.2f}s")

        if "api_fallback" in state:
            fb = state["api_fallback"]
            print(f"API Fallback: {fb.get('api_status')} ({fb.get('api_duration', 0):.2f}s)")

    print(f"\n{'=' * 80}\n")