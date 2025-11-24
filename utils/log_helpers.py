import inspect
import sys
import threading
import time

# Pytest va tizim freymlarini tashlash uchun filtrlar
_IGNORED_FUNCS = {
    '<module>', '__call__', '_multicall', '_hookexec',
    '_call_with_frames_removed', '_run_code', '_run_module_as_main',
    'inner', 'run', 'pytest_pyfunc_call'
}
_IGNORED_MODULES = ('pytest', 'importlib', 'runpy')

# Thread-local tracer holati (bitta tracer, ko'p target)
_TL = threading.local()


def _ensure_tracer_installed():
    """Bir marta (thread uchun) tracer o'rnatiladi; nested chaqiriqlar to'qnashmaydi."""
    if getattr(_TL, "tracer_installed", False):
        return
    _TL.tracer_installed = True
    _TL.targets = {}          # frame_id -> {'logger','method','label','t0'}
    _TL.prev_tracer = sys.gettrace()

    def _tracer(frame, event, arg):
        # mavjud tracer bo'lsa, uni ham chaqirib turamiz (PyCharm/pytest ichki tracerlari bilan moslik)
        if _TL.prev_tracer:
            try:
                _TL.prev_tracer(frame, event, arg)
            except Exception:
                pass

        tmap = _TL.targets
        fid = id(frame)

        if fid in tmap and event in ('return', 'exception'):
            info = tmap.pop(fid, None)
            if info:
                dt = time.time() - info['t0']
                method = info['method']
                label  = info['label']
                if event == 'exception':
                    # Exception turi (agar bo'lsa)
                    try:
                        exc_type = arg[0].__name__ if isinstance(arg, tuple) and arg and hasattr(arg[0], "__name__") else "Exception"
                    except Exception:
                        exc_type = "Exception"
                    info['logger'].debug(f"🔼==================== end: {method} - {label} (exc:{exc_type}, {dt:.2f}s) ====================🔼")
                else:
                    info['logger'].debug(f"🔼==================== end: {method} - {label} ({dt:.2f}s) ====================🔼")

        return _tracer

    sys.settrace(_tracer)


def _detect_page_name(stack):
    """Yaqin freymlardan self.__class__.__name__ ni topishga urinadi."""
    page_name = "UnknownPage"
    try:
        for idx in range(1, min(len(stack), 8)):
            frame_self = stack[idx].frame.f_locals.get("self", None)
            if frame_self is not None:
                page_name = getattr(getattr(frame_self, "__class__", None), "__name__", "UnknownPage")
                break
    except Exception:
        pass
    return page_name


def get_caller_chain(depth=5):
    """
    1) paramsiz: chaqirilgan funksiyadan joriy funksiyagacha bo'lgan zanjirni qaytaradi
       (pytest/tizim/_get_caller_chain tashlab ketiladi)
    2) depth=N: maksimal N ta funksiya (oxiridan) ko'rsatiladi.
    Format: "PageName → A → B → current"
    """
    try:
        stack = inspect.stack()
    except Exception:
        return "UnknownPage → stack_error"

    page_name = _detect_page_name(stack)
    chain = []

    try:
        for fr in stack[1:]:
            func = fr.function
            module = fr.frame.f_globals.get('__name__', '')

            # filtrlar
            if func in _IGNORED_FUNCS or any(m in module for m in _IGNORED_MODULES):
                continue
            if func == "_get_caller_chain":  # aynan shu helperni zanjirdan chiqaramiz
                continue
            if func.startswith("test_"):
                continue

            chain.append(func)
            if len(chain) >= depth:
                break
    except Exception:
        pass

    # Eng eski chaqiruvdan joriygacha tartiblash
    chain_str = " → ".join(reversed(chain)) if chain else "no_function_trace"
    return f"{page_name} → {chain_str}"


def _find_invoker_for(method_frame):
    """
    method_frame (masalan, BasePage.click) ni chaqirgan haqiqiy funksiyani (invoker) topadi.
    """
    try:
        stack = inspect.stack()
        # method_frame qaysi indeksda?
        idx = next((i for i, fr in enumerate(stack) if fr.frame is method_frame), None)
        if idx is None:
            return "unknown"
        # method_frame dan yuqoriga chiqib, birinchi haqiqiy (filtrdan o'tgan) funksiya nomini olamiz
        for fr in stack[idx+1:]:
            func = fr.function
            module = fr.frame.f_globals.get('__name__', '')
            if func in _IGNORED_FUNCS or any(m in module for m in _IGNORED_MODULES):
                continue
            if func.startswith("test_"):
                continue
            return func
    except Exception:
        pass
    return "unknown"


def log_start_end_for_current_method(logger, label=None, use_invoker=False):
    """
    2) invoker_name=True: ===== start: <method> - <invoker> =====
       ... va metod tugaganda ===== end: <method> - <invoker> =====
    3) log_name="name": ===== start: <method> - name ===== ... ===== end: <method> - name =====
       (label berilsa invoker e'tiborga olinmaydi)

    Eslatma: Bu funksiya _get_caller_chain(...) ichidan chaqiriladi.
    """
    _ensure_tracer_installed()

    # _get_caller_chain -> bu funksiya: demak 2 qadam yuqori — haqiqiy BasePage metod
    chain_wrapper = inspect.currentframe().f_back     # _get_caller_chain
    if chain_wrapper is None:
        return
    method_frame = chain_wrapper.f_back or chain_wrapper

    method = getattr(method_frame.f_code, "co_name", "unknown_method")
    # label tanlash
    if label:
        final_label = label
    elif use_invoker:
        final_label = _find_invoker_for(method_frame)
    else:
        # Default: agar hech narsa bermasa ham invoker yozilsinmi? — Yo‘q, faqat label bo‘lsa.
        final_label = "unknown"

    # Ro'yxatdan o'tkazish va START log
    _TL.targets[id(method_frame)] = {
        "logger": logger,
        "method": method,
        "label": final_label,
        "t0": time.time(),
    }
    logger.debug(f"🔽==================== start: {method} - {final_label} ====================🔽")
