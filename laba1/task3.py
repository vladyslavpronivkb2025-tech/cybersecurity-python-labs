import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_PATH = os.path.join(DATA_DIR, "users.csv")
LOG_PATH = os.path.join(DATA_DIR, "log.json")

MIN_PASS_LEN = 12
SALT = f"{VARIANT_NUMBER:05d}"

USERS_TO_REGISTER = (
    ("alice_sec", "SecureP@ss123456jidjip3872890$%&*$#8(*&^%$#@!"),
    ("bob_admin", "AdminStrongP@ss2"),
    ("charlie_dev", "CharlieDev#2026"),
    ("diana_analyst", "DianaData@Secure"),
    ("edward_net", "NetworkDef!2026"),
    ("fiona_audit", "AuditAccess#999"),
    ("george_soc", "MonitoringP@ss1"),
    ("helen_cloud", "CloudSecureKey#7"),
    ("ian_crypto", "CryptoSafeP@ss8"),
    ("julia_test", "TestPassw0rd!12"),
)


class ValidationError(Exception):
    pass


def log_event(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = kwargs.get("username", args[0] if args else "unknown")
        result = "failure"
        try:
            res = func(*args, **kwargs)
            if res:
                result = "success"
            return res
        except Exception:
            result = "failure"
            raise
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": result,
                "timestamp": datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                ),
                "args": list(args),
                "kwargs": kwargs,
            }
            try:
                logs = []
                if os.path.exists(LOG_PATH):
                    with open(LOG_PATH, "r", encoding="utf-8") as f:
                        try:
                            logs = json.load(f)
                        except json.JSONDecodeError:
                            logs = []
                logs.append(log_entry)
                with open(LOG_PATH, "w", encoding="utf-8") as f:
                    json.dump(logs, f, indent=4, ensure_ascii=False)
            except OSError as err:
                print(f"[Помилка запису в журнал]: {err}")

    return wrapper


def generate_hash(password, salt="00000"):
    if password is None or salt is None or password == "" or salt == "":
        raise ValueError("Пароль та сіль не можуть бути порожніми")
    if len(password) < MIN_PASS_LEN:
        raise ValidationError(f"Пароль закороткий (< {MIN_PASS_LEN} символів)")

    salted_data = (password + salt).encode("utf-8")
    return hashlib.sha3_512(salted_data).hexdigest()


def create_user(username, password):
    return username, generate_hash(password, salt=SALT)


def create_users(users_list):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash"])
            for u_name, pwd in users_list:
                _, p_hash = create_user(u_name, pwd)
                writer.writerow([u_name, p_hash])
    except OSError as err:
        print(f"[Помилка створення CSV]: {err}")


def read_users_db():
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print("[Помилка]: Файл users.csv не знайдено")
        return []
    except OSError as err:
        print(f"[Помилка читання CSV]: {err}")
        return []


@log_event
def login(username, password):
    if not username or not password:
        raise ValueError("Логін та пароль є обов'язковими для входу")

    input_hash = generate_hash(password, salt=SALT)
    users_db = read_users_db()
    for record in users_db:
        if record["username"] == username:
            return record["password_hash"] == input_hash
    return False


def run_task3():
    print("=" * 65)
    print(f"Завдання 3 | Студент: {STUDENT_NAME} (Варіант {VARIANT_NUMBER})")
    print("=" * 65)

    print("[1] Створення файлу data/users.csv...")
    create_users(USERS_TO_REGISTER)

    print("\n[2] Вміст зареєстрованої бази користувачів:")
    db = read_users_db()
    print(f"{'Користувач':<18} | {'Хеш SHA3-512 (перші 28 символів)':<30}")
    print("-" * 52)
    for row in db:
        print(f"{row['username']:<18} | {row['password_hash'][:28]}...")

    print("\n[3] Тестування автентифікації та запису в log.json:")
    test_cases = [
        ("alice_sec", "SecureP@ss123456"),
        ("alice_sec", "WrongPassword!123"),
        ("ghost_user", "SomeSecret#12345"),
    ]

    for user, pwd in test_cases:
        try:
            status = login(user, pwd)
            result_str = "УСПІХ" if status else "НЕВДАЧА"
            print(f" - Вхід користувача '{user}': {result_str}")
        except (ValidationError, ValueError) as err:
            print(f" - Вхід '{user}' відхилено: {err}")

    print("\n[4] Тест обробки винятку (закороткий пароль):")
    try:
        generate_hash("short", salt=SALT)
    except ValidationError as exc:
        print(f" - Успішно перехоплено виняток: ValidationError -> {exc}")
    print()


if __name__ == "__main__":
    run_task3()
