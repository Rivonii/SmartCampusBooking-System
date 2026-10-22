


CAMPUS_RULES = {
    "Campus A": {
        "opening_time": "08:00",
        "closing_time": "17:00",
        "max_duration": 2
    },
    "Campus B": {
        "opening_time": "08:00",
        "closing_time": "18:00",
        "max_duration": 3
    },
    "Campus C": {
        "opening_time": "09:00",
        "closing_time": "16:00",
        "max_duration": 1
    }
}


def check_booking_rules(campus_name, start_time, duration):



    if campus_name not in CAMPUS_RULES:
        return False, "Campus not found."

    rules = CAMPUS_RULES[campus_name]


    try:
        duration = int(duration)

        if duration < 1:
            return False, "Duration must be at least 1 hour."
        if duration > rules["max_duration"]:
            return False, (
                f"{campus_name} allows a maximum booking "
                f"duration of {rules['max_duration']} hour(s)."
            )

    except (ValueError, TypeError):
        return False, "Please enter a valid booking duration."




    try:
        from datetime import datetime

        start_time = datetime.strptime(
            start_time,
            "%H:%M"
        ).strftime("%H:%M")

    except (ValueError, TypeError):
        return False, "Please enter a valid start time in HH:MM format."


    start_minutes = (
        int(start_time[:2]) * 60
        + int(start_time[3:5])
    )

    opening_minutes = (
        int(rules["opening_time"][:2]) * 60
        + int(rules["opening_time"][3:5])
    )

    closing_minutes = (
        int(rules["closing_time"][:2]) * 60
        + int(rules["closing_time"][3:5])
    )


    if start_minutes < opening_minutes:
        return False, "Booking starts before campus opening time."


    if start_minutes + duration * 60 > closing_minutes:
        return False, "Booking ends after campus closing time."

    return True, "Booking follows campus rules."
