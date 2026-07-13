import random
import pytest
from apis.robot_api import RobotAPI
from apis.role_api import RoleAPI
from apis.natural_person_api import NaturalPersonAPI
from apis.user_api import UserAPI
from apis.room_api import RoomAPI
from utils.env_reader import get_env

ROBOT_COUNT = 100
ROOM_COUNT = 150   # bitta robotga biriktiriladigan room soni
NP_IMPORT_CHUNK = 50  # bitta natural_person import so'rovidagi maksimal soni

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(7)
def test_robot_save(save_data, load_data):
    api = RobotAPI(load_data, auth_profile="admin")

    code = load_data("api/code")
    robot_code = f"api_robot_cod-{code}"
    robot_name = f"api_robot-{code}"
    room_id = load_data("api/room_id")
    admin_id = _get_role_id(load_data, "Админ")

    body = {
      "code": robot_code,
      "name": robot_name,
      "state": "A",
      "tracking_enabled": "N",
      "role_ids": [admin_id],
      "room_ids": [room_id]
    }

    resp, t_network, t_total = api.import_robot(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_name = data["name"]
    assert robot_name == get_name, f"robot_name: {robot_name} != get_name: {get_name}"

    get_robot_id = data["robot_id"]
    save_data("api/robot_id", get_robot_id)
    save_data("api/admin_id", admin_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(9)
def test_robot_save_bulk(save_data, load_data):
    """ROBOT_COUNT ta robotni har xil name (va code) bilan yaratadi."""
    api = RobotAPI(load_data, auth_profile="admin")

    # Bir marta olinadi — hamma robot uchun umumiy
    code = load_data("api/code") or str(random.randint(100000, 999999))
    room_id = load_data("api/room_id")
    assert room_id, "api/room_id topilmadi — avval Room flow'ini ishga tushiring (test_room_save)."
    # api/role_id berilgan bo'lsa o'shani ishlatadi, aks holda "Админ" rolini qidiradi
    role_id = load_data("api/role_id") or _get_role_id(load_data, "Админ")

    created = []
    for i in range(1, ROBOT_COUNT + 1):
        robot_code = f"api_robot_cod-{code}-{i}"
        robot_name = f"api_robot-{code}-{i}"

        body = {
            "code": robot_code,
            "name": robot_name,
            "state": "A",
            "tracking_enabled": "N",
            "role_ids": [role_id],
            "room_ids": [room_id],
        }

        resp, t_network, t_total = api.import_robot(body)
        data = api.handle_response(resp, t_network, t_total, body=body)

        get_name = data["name"]
        assert robot_name == get_name, f"robot_name: {robot_name} != get_name: {get_name}"

        created.append({"robot_id": data["robot_id"], "name": robot_name})

    save_data("api/role_id", role_id)
    save_data("api/robot_bulk", created)

    assert len(created) == ROBOT_COUNT, f"Yaratilgan robotlar: {len(created)} != {ROBOT_COUNT}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(10)
def test_robot_save_bulk_with_person(save_data, load_data):
    """ROBOT_COUNT ta natural person yaratadi va har birini person_id orqali robotga bog'laydi.

    Eslatma: person_id berilganda role_ids YUBORILMAYDI — rollar foydalanuvchiga (user)
    tegishli, natural person esa user emas, aks holda server 500 qaytaradi.
    """
    np_api = NaturalPersonAPI(load_data, auth_profile="admin")
    robot_api = RobotAPI(load_data, auth_profile="admin")

    room_id = load_data("api/room_id")
    assert room_id, "api/room_id topilmadi."

    base = str(random.randint(100000, 999999))
    np_codes = [f"api_np-{base}-{i}" for i in range(1, ROBOT_COUNT + 1)]

    # 1) Natural person'larni yaratish (limit sababli bo'laklarga bo'lib)
    for start in range(0, len(np_codes), NP_IMPORT_CHUNK):
        chunk = np_codes[start:start + NP_IMPORT_CHUNK]
        body = {
            "natural_person": [
                {"first_name": c, "code": c, "is_budgetarian": "N", "state": "A", "groups": []}
                for c in chunk
            ]
        }
        resp, t_network, t_total = np_api.import_natural_person(body)
        np_api.handle_response(resp, t_network, t_total, body=body)

    # 2) person_id'larni olish: bitta umumiy export -> {code: person_id}, kerak bo'lsa code bo'yicha fallback
    resp, t_network, t_total = np_api.export_natural_person({
        "rooms": [{"room_code": ""}], "code": "",
        "begin_created_on": "", "end_created_on": "",
        "begin_modified_on": "", "end_modified_on": "",
    })
    data = np_api.handle_response(resp, t_network, t_total)
    code_to_pid = {p["code"]: p["person_id"] for p in data.get("natural_person", [])}

    person_ids = []
    for c in np_codes:
        pid = code_to_pid.get(c)
        if pid is None:
            r, n, t = np_api.export_natural_person({
                "rooms": [{"room_code": ""}], "code": c,
                "begin_created_on": "", "end_created_on": "",
                "begin_modified_on": "", "end_modified_on": "",
            })
            d = np_api.handle_response(r, n, t)
            pid = d["natural_person"][0]["person_id"]
        person_ids.append(pid)

    assert len(person_ids) == ROBOT_COUNT, f"person_id soni: {len(person_ids)} != {ROBOT_COUNT}"

    # 3) Har bir person_id uchun robot yaratish
    created = []
    for i, pid in enumerate(person_ids, start=1):
        robot_code = f"api_robot_cod-{base}-{i}"
        robot_name = f"api_robot-{base}-{i}"

        body = {
            "person_id": pid,
            "code": robot_code,
            "name": robot_name,
            "state": "A",
            "tracking_enabled": "N",
            "room_ids": [room_id],
        }

        resp, t_network, t_total = robot_api.import_robot(body)
        d = robot_api.handle_response(resp, t_network, t_total, body=body)

        get_name = d["name"]
        assert robot_name == get_name, f"robot_name: {robot_name} != get_name: {get_name}"

        created.append({"robot_id": d["robot_id"], "name": robot_name, "person_id": pid})

    save_data("api/robot_person_bulk", created)

    assert len(created) == ROBOT_COUNT, f"Yaratilgan robotlar: {len(created)} != {ROBOT_COUNT}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(11)
def test_robot_save_bulk_person_role(save_data, load_data):
    """ROBOT_COUNT ta robotni ham person, ham rol bilan yaratadi.

    Smartup'da bitta robot+add:save chaqiruvida person_id va role birga ishlamaydi
    (person hali user bo'lmagani uchun server 500 qaytaradi). Shuning uchun har biri uchun:
        1) natural person yaratiladi -> person_id
        2) robot yaratiladi (role_ids bilan, personsiz) -> robot_id  (rol robotga ulanadi)
        3) user yaratiladi (user_id=person_id, robot_id=[robot_id]) -> person robotga bog'lanadi
    Natijada har staff: person + rol bilan.
    """
    np_api = NaturalPersonAPI(load_data, auth_profile="admin")
    robot_api = RobotAPI(load_data, auth_profile="admin")
    user_api = UserAPI(load_data, auth_profile="admin")

    room_id = load_data("api/room_id")
    assert room_id, "api/room_id topilmadi."
    role_id = load_data("api/role_id") or _get_role_id(load_data, "Админ")
    password = get_env("PASSWORD_USER")
    assert password, "PASSWORD_USER (.env) topilmadi."

    base = str(random.randint(100000, 999999))
    np_codes = [f"api_np-{base}-{i}" for i in range(1, ROBOT_COUNT + 1)]

    # 1) Natural person'larni yaratish (limit sababli bo'laklarga bo'lib)
    for start in range(0, len(np_codes), NP_IMPORT_CHUNK):
        chunk = np_codes[start:start + NP_IMPORT_CHUNK]
        body = {
            "natural_person": [
                {"first_name": c, "code": c, "is_budgetarian": "N", "state": "A", "groups": []}
                for c in chunk
            ]
        }
        resp, t_network, t_total = np_api.import_natural_person(body)
        np_api.handle_response(resp, t_network, t_total, body=body)

    # 2) person_id'larni olish (bitta umumiy export -> map, kerak bo'lsa code bo'yicha fallback)
    resp, t_network, t_total = np_api.export_natural_person({
        "rooms": [{"room_code": ""}], "code": "",
        "begin_created_on": "", "end_created_on": "",
        "begin_modified_on": "", "end_modified_on": "",
    })
    data = np_api.handle_response(resp, t_network, t_total)
    code_to_pid = {p["code"]: p["person_id"] for p in data.get("natural_person", [])}

    person_ids = []
    for c in np_codes:
        pid = code_to_pid.get(c)
        if pid is None:
            r, n, t = np_api.export_natural_person({
                "rooms": [{"room_code": ""}], "code": c,
                "begin_created_on": "", "end_created_on": "",
                "begin_modified_on": "", "end_modified_on": "",
            })
            d = np_api.handle_response(r, n, t)
            pid = d["natural_person"][0]["person_id"]
        person_ids.append(pid)

    assert len(person_ids) == ROBOT_COUNT, f"person_id soni: {len(person_ids)} != {ROBOT_COUNT}"

    # 3) Har bir person uchun: robot (rol bilan) -> user (person bog'lash)
    created = []
    for i, pid in enumerate(person_ids, start=1):
        robot_code = f"api_robot_cod-{base}-{i}"
        robot_name = f"api_robot-{base}-{i}"

        robot_body = {
            "code": robot_code,
            "name": robot_name,
            "state": "A",
            "tracking_enabled": "N",
            "role_ids": [role_id],
            "room_ids": [room_id],
        }
        resp, t_network, t_total = robot_api.import_robot(robot_body)
        rd = robot_api.handle_response(resp, t_network, t_total, body=robot_body)
        robot_id = rd["robot_id"]

        user_body = {
            "user_id": pid,
            "name": robot_name,
            "login": f"api_login-{base}-{i}",
            "code": f"api_uc-{base}-{i}",
            "email": "",
            "gender": "",
            "password": password,
            "photo_sha": "",
            "robot_id": [robot_id],
            "role_id": [],
            "state": "A",
        }
        resp, t_network, t_total = user_api.user_add(user_body)
        ud = user_api.handle_response(resp, t_network, t_total, body=user_body)

        created.append({
            "robot_id": robot_id,
            "robot_name": robot_name,
            "person_id": pid,
            "user_id": ud["user_id"],
            "role_id": role_id,
        })

    save_data("api/robot_person_role_bulk", created)

    assert len(created) == ROBOT_COUNT, f"Yaratilgan robotlar: {len(created)} != {ROBOT_COUNT}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(12)
def test_robot_with_many_rooms(save_data, load_data):
    """ROOM_COUNT ta room yaratadi va hammasini bitta robotga biriktiradi.

    Robot person + rol bilan ham jihozlanadi (boshqa testlardagi kabi):
        1) ROOM_COUNT ta room yaratiladi -> room_ids
        2) natural person yaratiladi -> person_id
        3) robot yaratiladi (role_ids + barcha room_ids, personsiz) -> robot_id
        4) user yaratiladi (user_id=person_id, robot_id=[robot_id]) -> person robotga bog'lanadi
        5) robot robot_view:model orqali o'qiladi va tekshiriladi/ko'rsatiladi
    """
    room_api = RoomAPI(load_data, auth_profile="admin")
    np_api = NaturalPersonAPI(load_data, auth_profile="admin")
    robot_api = RobotAPI(load_data, auth_profile="admin")
    user_api = UserAPI(load_data, auth_profile="admin")

    role_id = load_data("api/role_id") or _get_role_id(load_data, "Админ")
    password = get_env("PASSWORD_USER")
    assert password, "PASSWORD_USER (.env) topilmadi."

    base = str(random.randint(100000, 999999))

    # 1) ROOM_COUNT ta room yaratish
    room_ids = []
    for i in range(1, ROOM_COUNT + 1):
        body = {
            "code": f"api_room-{base}-{i}",
            "name": f"api_room-{base}-{i}",
            "room_kind": "D",
            "state": "A",
        }
        resp, t_network, t_total = room_api.import_room(body)
        d = room_api.handle_response(resp, t_network, t_total, body=body)
        room_ids.append(d["room_id"])

    assert len(room_ids) == ROOM_COUNT, f"Room soni: {len(room_ids)} != {ROOM_COUNT}"

    # 2) natural person -> person_id
    np_code = f"api_np-{base}"
    np_body = {"natural_person": [
        {"first_name": np_code, "code": np_code, "is_budgetarian": "N", "state": "A", "groups": []}
    ]}
    resp, t_network, t_total = np_api.import_natural_person(np_body)
    np_api.handle_response(resp, t_network, t_total, body=np_body)

    resp, t_network, t_total = np_api.export_natural_person({
        "rooms": [{"room_code": ""}], "code": np_code,
        "begin_created_on": "", "end_created_on": "",
        "begin_modified_on": "", "end_modified_on": "",
    })
    person_id = np_api.handle_response(resp, t_network, t_total)["natural_person"][0]["person_id"]

    # 3) robot: rol + barcha room (personsiz)
    robot_name = f"api_robot_rooms-{base}"
    robot_body = {
        "code": robot_name,
        "name": robot_name,
        "state": "A",
        "tracking_enabled": "N",
        "role_ids": [role_id],
        "room_ids": room_ids,
    }
    resp, t_network, t_total = robot_api.import_robot(robot_body)
    robot_id = robot_api.handle_response(resp, t_network, t_total, body=robot_body)["robot_id"]

    # 4) user: person'ni robotga bog'lash
    user_body = {
        "user_id": person_id,
        "name": robot_name,
        "login": f"api_login-{base}",
        "code": f"api_uc-{base}",
        "email": "", "gender": "", "password": password, "photo_sha": "",
        "robot_id": [robot_id],
        "role_id": [],
        "state": "A",
    }
    resp, t_network, t_total = user_api.user_add(user_body)
    user_api.handle_response(resp, t_network, t_total, body=user_body)

    # 5) robotni o'qish va ko'rsatish
    resp, t_network, t_total = robot_api.view_robot({"robot_id": robot_id})
    view = robot_api.handle_response(resp, t_network, t_total, body={"robot_id": robot_id})
    info = view[2]
    attached_rooms = [r for r in info.get("room_names", "").split(", ") if r]

    robot_api.logger.info("=" * 70)
    robot_api.logger.info(f"ROBOT KO'RINISHI: robot_id={robot_id}")
    robot_api.logger.info(f"  name        : {info.get('name')}")
    robot_api.logger.info(f"  code        : {info.get('code')}")
    robot_api.logger.info(f"  role_names  : {info.get('role_names')}")
    robot_api.logger.info(f"  person_names: {info.get('person_names')}")
    robot_api.logger.info(f"  room soni   : {len(attached_rooms)}")
    robot_api.logger.info("=" * 70)

    save_data("api/rooms_robot_id", robot_id)
    save_data("api/rooms_robot_room_ids", room_ids)
    save_data("api/rooms_robot_person_id", person_id)

    assert len(attached_rooms) == ROOM_COUNT, \
        f"Robotga biriktirilgan room: {len(attached_rooms)} != {ROOM_COUNT}"
    assert info.get("role_names"), "Robotga rol biriktirilmagan!"
    assert info.get("person_names"), "Robotga person biriktirilmagan!"

# ----------------------------------------------------------------------------------------------------------------------

def _get_role_id(load_data, role_name):
    api = RoleAPI(load_data, auth_profile="admin")
    body = {
        "p": {
            "column": ["role_id", "name"],
            "filter": ["name", "=", role_name],
            "limit": 1,
            "offset": 0,
            "sort": []
        }
    }

    resp, t_network, t_total = api.role_list(body)
    data = api.handle_response(resp, t_network, t_total, body=body)
    rows = data.get("data") or []

    if not rows:
        raise AssertionError(f"Role topilmadi: {role_name}")

    return rows[0][0]

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(8)
def test_robot_model(load_data):
    api = RobotAPI(load_data, auth_profile="admin")

    robot_id = load_data("api/robot_id")

    body = {
        "robot_id": robot_id
    }

    resp, t_network, t_total = api.export_robot(body)

    api.handle_response(resp, t_network, t_total, body=body)

# ----------------------------------------------------------------------------------------------------------------------
