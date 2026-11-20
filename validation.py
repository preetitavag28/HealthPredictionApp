
import re
from datetime import datetime, date


def validate_name(name):
    return bool(name and name.strip())


def validate_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email.strip()))


def validate_dob(dob):
    """
    Accept DD/MM/YYYY and DD.MM.YYYY.
    Reject impossible and future dates.
    """

    try:
        dob = dob.strip()

        if "/" in dob:
            parsed_date = datetime.strptime(
                dob, "%d/%m/%Y"
            ).date()

        elif "." in dob:
            parsed_date = datetime.strptime(
                dob, "%d.%m.%Y"
            ).date()

        else:
            return False, "Use DD/MM/YYYY format."

        if parsed_date > date.today():
            return False, "Date of birth cannot be in the future."

        return True, "Valid date."

    except ValueError:
        return False, "Invalid calendar date."


def validate_number(value, field_name):
    try:
        number = float(value)

        if not (number >= 0 and number < float("inf")):
            return False, f"{field_name} must be a finite, non-negative number."

        return True, number

    except (ValueError, TypeError):
        return False, f"{field_name} must be numeric."
