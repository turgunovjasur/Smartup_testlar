import functools
import json
import time
from datetime import datetime
from pathlib import Path
from conftest import cleanup_driver, create_driver
from utils.logger import configure_logging

# ======================================================================================================================
# Test State Manager
# ======================================================================================================================

class TestStateManager:
    """Test holatlarini boshqarish va saqlash"""

    def __init__(self, state_file="test_state.json"):
        self.state_file = Path(state_file)
        self.states = self._load_states()

    def _load_states(self):
        """Mavjud test holatlarini yuklash"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_states(self):
        """Test holatlarini faylga saqlash"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.states, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Test holatini saqlashda xatolik: {e}")

    def get_state(self, test_name):
        """Test holatini olish"""
        return self.states.get(test_name, {})

    def update_state(self, test_name, status, attempt=1, error=None, duration=None):
        """Test holatini yangilash"""
        self.states[test_name] = {
            "status": status,
            "attempt": attempt,
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(error) if error else None,
            "duration": duration
        }
        self._save_states()

    def is_passed(self, test_name):
        """Test muvaffaqiyatli o'tganmi?"""
        state = self.get_state(test_name)
        return state.get("status") == "PASSED"

    def reset_state(self, test_name):
        """Test holatini qayta tiklash"""
        if test_name in self.states:
            del self.states[test_name]
            self._save_states()

    def reset_all_states(self):
        """Barcha test holatlarini tozalash"""
        self.states = {}
        self._save_states()

    def get_summary(self):
        """Test holatlarining qisqacha xulosasi"""
        passed = sum(1 for s in self.states.values() if s.get("status") == "PASSED")
        failed = sum(1 for s in self.states.values() if s.get("status") == "FAILED")
        total = len(self.states)

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{(passed / total * 100):.1f}%" if total > 0 else "0%"
        }

# ==================================================================================================================
# Retry Decorator
# ==================================================================================================================

def retry_on_failure(retry_count=2, retry_delay=5, dependencies=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Test nomini olish
            test_name = func.__name__
            logger = configure_logging(test_name)

            # State manager yaratish
            state_manager = TestStateManager()

            # Argumentlardan driver va test_data ni topish
            driver = kwargs.get('driver') or (args[0] if len(args) > 0 else None)
            test_data = kwargs.get('test_data') or (args[1] if len(args) > 1 else None)

            if not driver or not test_data:
                raise ValueError(f"{test_name}: 'driver' va 'test_data' argumentlari topilmadi")

            # Dependency tekshirish
            if dependencies:
                missing_deps = []
                for dep in dependencies:
                    if not state_manager.is_passed(dep):
                        missing_deps.append(dep)

                if missing_deps:
                    msg = f"⭐️ {test_name} SKIPPED - Dependencies PASSED emas: {missing_deps}"
                    print(msg)
                    state_manager.update_state(test_name, "SKIPPED", error=msg)

                    import pytest
                    pytest.skip(msg)

            # Retry loop
            last_exception = None
            current_driver = driver  # Birinchi urinishda fixture driver
            user_data_dir = None
            start_time = time.time()

            for attempt in range(1, retry_count + 1):
                # 2-urinishdan boshlab yangi driver yaratish
                if attempt > 1:
                    logger.info(f"🔧 Yangi driver yaratilmoqda (urinish {attempt})...")
                    current_driver, user_data_dir, start_time = create_driver(test_name, test_data)

                    # kwargs/args da driver ni yangilash
                    if 'driver' in kwargs:
                        kwargs['driver'] = current_driver
                    else:
                        # args tuple, uni list ga o'tkazing
                        args_list = list(args)
                        args_list[0] = current_driver
                        args = tuple(args_list)

                try:
                    print(f"\n{'=' * 70}")
                    print(f"🔄 {test_name} - Urinish {attempt}/{retry_count}")
                    print(f"{'=' * 70}")

                    # Test funksiyasini ishga tushirish
                    result = func(*args, **kwargs)

                    # Test muvaffaqiyatli o'tdi
                    duration = time.time() - start_time
                    state_manager.update_state(
                        test_name,
                        "PASSED",
                        attempt=attempt,
                        duration=duration
                    )

                    print(f"\n✅ {test_name} PASSED (urinish: {attempt}, vaqt: {duration:.2f}s)")

                    # Yangi yaratilgan driver'ni tozalash (birinchi urinish emas bo'lsa)
                    if attempt > 1 and current_driver:
                        cleanup_driver(current_driver, user_data_dir, logger, start_time, test_name)

                    return result

                except Exception as e:
                    last_exception = e
                    duration = time.time() - start_time

                    logger.error(f"❌ Urinish {attempt}/{retry_count} FAILED: {str(e)}")

                    # Driver'ni yopish
                    try:
                        if attempt == 1:
                            # Birinchi driver (fixture'dan kelgan)
                            logger.info("🔒 Birinchi driver yopilmoqda...")
                            driver.quit()
                            logger.info("✅ Birinchi driver yopildi")
                        else:
                            # Yangi yaratilgan driver
                            logger.info("🔒 Yangi driver tozalanmoqda...")
                            cleanup_driver(current_driver, user_data_dir, logger, start_time, test_name)
                            logger.info("✅ Yangi driver tozalandi")
                    except Exception as cleanup_error:
                        logger.warning(f"⚠️ Driver yopishda xatolik: {cleanup_error}")

                    if attempt == retry_count:
                        # Oxirgi urinish ham fail
                        state_manager.update_state(
                            test_name,
                            "FAILED",
                            attempt=attempt,
                            error=str(e),
                            duration=duration
                        )

                        print(f"\n❌ {test_name} FAILED - Barcha {retry_count} urinish ham muvaffaqiyatsiz")
                        print(f"   Xatolik: {str(e)}")
                        raise last_exception
                    else:
                        # Keyingi urinish
                        print(f"\n⚠️  {test_name} FAILED (urinish: {attempt}/{retry_count})")
                        print(f"   Xatolik: {str(e)}")
                        print(f"   ⏳ {retry_delay} sekund kutish keyin qayta urinish...\n")

                        state_manager.update_state(
                            test_name,
                            "RETRY",
                            attempt=attempt,
                            error=str(e),
                            duration=duration
                        )

                        time.sleep(retry_delay)

        return wrapper

    return decorator

# ==================================================================================================================
# Helper Functions
# ==================================================================================================================

def reset_test_state(test_name=None):
    """
    Test holatini qayta tiklash

    Parameters:
    -----------
    test_name : str, optional
        Muayyan test nomini tiklash. Agar None bo'lsa, barchasi tiklanadi.
    """
    state_manager = TestStateManager()

    if test_name:
        state_manager.reset_state(test_name)
        print(f"✅ {test_name} holati qayta tiklandi")
    else:
        state_manager.reset_all_states()
        print(f"✅ Barcha test holatlari qayta tiklandi")

# ======================================================================================================================

def get_test_summary():
    """Test holatlarining qisqacha xulosasi"""
    state_manager = TestStateManager()
    summary = state_manager.get_summary()

    print(f"\n{'=' * 50}")
    print(f"📊 TEST HOLATLARI XULOSASI")
    print(f"{'=' * 50}")
    print(f"Jami testlar:     {summary['total']}")
    print(f"✅ Passed:        {summary['passed']}")
    print(f"❌ Failed:        {summary['failed']}")
    print(f"📈 Pass rate:     {summary['pass_rate']}")
    print(f"{'=' * 50}\n")

    return summary

# ======================================================================================================================

def print_test_states():
    """Barcha test holatlarini chop etish"""
    state_manager = TestStateManager()

    if not state_manager.states:
        print("ℹ️  Hech qanday test holati topilmadi")
        return

    print(f"\n{'=' * 80}")
    print(f"📋 BARCHA TEST HOLATLARI")
    print(f"{'=' * 80}")

    for test_name, state in state_manager.states.items():
        status_emoji = {
            "PASSED": "✅",
            "FAILED": "❌",
            "SKIPPED": "⭐️",
            "RETRY": "🔄"
        }.get(state.get("status"), "❓")

        print(f"\n{status_emoji} {test_name}")
        print(f"   Status:    {state.get('status')}")
        print(f"   Attempt:   {state.get('attempt')}")
        print(f"   Last Run:  {state.get('last_run')}")

        if state.get('duration'):
            print(f"   Duration:  {state.get('duration'):.2f}s")

        if state.get('error'):
            error_msg = state.get('error')
            # Xatolikni qisqartirish (birinchi 100 belgi)
            if len(error_msg) > 100:
                error_msg = error_msg[:97] + "..."
            print(f"   Error:     {error_msg}")

    print(f"\n{'=' * 80}\n")

# ======================================================================================================================
