import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

PASSWORDS = [
    "password123",
    "Qwerty!2023",
    "admin",
    "MyP@ssword",
    "123456",
    "SecurePass!",
    "test",
    "P@ssword123",
    "welcome",
    "StrongP@ss1",
]

CRITERIA = {
    "min_length": 8,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

FORBIDDEN_PASSWORDS = {
    "password",
    "123456",
    "admin",
    "test",
    "welcome",
    "qwerty",
}

SPECIAL_CHARACTERS = set("!@#$%^&*()-_=+[]{}|;:,.<>?/")


def evaluate_password(
    pwd: str,
    all_passwords: list[str],
    criteria: dict,
    forbidden: set[str],
):
    min_len = criteria["min_length"]

    if pwd in forbidden or len(pwd) < min_len:
        return "Заборонений"
    has_digit = any(c.isdigit() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_spec = any(c in SPECIAL_CHARACTERS for c in pwd)

    all_req_met = has_digit and has_upper and has_spec
    any_met = has_digit or has_upper or has_lower or has_spec

    if pwd in forbidden or len(pwd) < min_len:
        return "Заборонений"

    has_digit = any(c.isdigit() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_spec = any(c in SPECIAL_CHARACTERS for c in pwd)

    all_req_met = has_digit and has_upper and has_spec
    any_met = has_digit or has_upper or has_lower or has_spec

    if all_req_met:
        is_unique = all_passwords.count(pwd) == 1
        if len(pwd) >= min_len + 4 and is_unique:
            return "Дуже сильний"
        return "Сильний"

    if len(pwd) >= min_len and (has_digit or has_upper or has_spec):
        return "Середній"

    if any_met:
        return "Слабкий"

    return "Заборонений"


def run_task1():
    print("=" * 65)
    print(f"Завдання 1 | Студент: {STUDENT_NAME} (Варіант {VARIANT_NUMBER})")
    print("=" * 65)

    work_list = list(PASSWORDS)

    random.seed(VARIANT_NUMBER)
    random_indices = [random.randint(0, len(PASSWORDS) - 1) for _ in range(3)]
    for idx in random_indices:
        work_list.append(PASSWORDS[idx])

    print(f"{'Пароль':<20} | {'Довжина':<8} | {'Статус':<15}")
    print("-" * 65)
    for pwd in work_list:
        status = evaluate_password(pwd, work_list, CRITERIA, FORBIDDEN_PASSWORDS)
        print(f"{pwd:<20} | {len(pwd):<8} | {status:<15}")
    print()


if __name__ == "__main__":
    run_task1()
