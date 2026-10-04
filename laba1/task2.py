import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

USERS = {
    "admin001": {
        "role": "administrator",
        "clearance": 4,
        "department": "IT",
        "active": True,
    },
    "user123": {
        "role": "analyst",
        "clearance": 2,
        "department": "Security",
        "active": True,
    },
    "guest789": {
        "role": "guest",
        "clearance": 1,
        "department": "External",
        "active": True,
    },
    "manager456": {
        "role": "manager",
        "clearance": 3,
        "department": "Operations",
        "active": True,
    },
    "contractor99": {
        "role": "contractor",
        "clearance": 1,
        "department": "External",
        "active": False,
    },
}

RESOURCES = [
    ("database_backup", 4),
    ("user_logs", 2),
    ("public_docs", 1),
    ("financial_reports", 3),
    ("system_config", 4),
    ("training_materials", 1),
    ("security_policies", 3),
    ("audit_logs", 4),
    ("employee_data", 3),
    ("temp_files", 1),
]

SECURITY_LEVELS = ("Public", "Internal", "Confidential", "Secret")
BLOCKED_USERS = {"contractor99", "temp_user", "suspended_acc"}


def check_access(username, resource_name, res_level):

    if username not in USERS:
        return "DENY (User not found)"

    if username in BLOCKED_USERS:
        return "DENY (User is blocked)"

    user_info = USERS[username]

    if not user_info["active"]:
        return "DENY (Account inactive)"

    if user_info["clearance"] >= res_level:
        return "ALLOW"
    else:
        return "DENY (Insufficient clearance)"


def run_task2():
    print("=" * 65)
    print(f"Завдання 2 | Студент: {STUDENT_NAME} (Варіант {VARIANT_NUMBER})")
    print("=" * 65)

    print("СПИСОК РЕСУРСІВ:")
    for res_name, lvl in RESOURCES:
        lvl_name = SECURITY_LEVELS[lvl - 1]
        print(f" - {res_name:<22}: {lvl_name} (Рівень {lvl})")

    print("\nРЕЗУЛЬТАТИ ПЕРЕВІРКИ ДОСТУПУ:")

    for username in USERS:
        for res_name, res_level in RESOURCES:
            result = check_access(username, res_name, res_level)
            print(f"user={username:<13} resource={res_name:<20} -> {result}")
    print()


if __name__ == "__main__":
    run_task2()
