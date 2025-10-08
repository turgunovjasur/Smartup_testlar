# apis/response_utils.py
import json

def detect_response_type(resp):
    """Javob turini aniqlaydi: json | text | html | xml | binary"""
    ctype_full = (resp.headers.get("Content-Type") or "").lower()
    ctype = ctype_full.split(";")[0].strip()

    if "application/json" in ctype:
        return "json"
    if ctype.startswith("text/"):
        return "text"
    if "html" in ctype:
        return "html"
    if "xml" in ctype:
        return "xml"
    if "octet-stream" in ctype or ctype == "":
        try:
            _ = resp.json()
            return "json"
        except Exception:
            return "text"
    return "binary"


# def parse_response(resp):
#     """(data, rtype) qaytaradi."""
#     rtype = detect_response_type(resp)
#     try:
#         if rtype == "json":
#             return resp.json(), "json"
#         if rtype in ("text", "html", "xml"):
#             return resp.text, rtype
#         return resp.content, "binary"
#     except requests.exceptions.JSONDecodeError:
#         return resp.text, "text"


def pretty_body(resp) -> str:
    """Har doim server yuborgan asl body’ni qaytaradi."""
    try:
        rtype = detect_response_type(resp)
        if rtype == "json":
            return json.dumps(resp.json(), ensure_ascii=False, indent=2)
        elif rtype in ("text", "html", "xml"):
            return resp.text or "<no response>"
        else:
            size = len(resp.content or b"")
            ctype = resp.headers.get("Content-Type") or "binary"
            return f"<{ctype} {size} bytes>"
    except Exception:
        return resp.text or "<no response>"
