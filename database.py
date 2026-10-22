
import sqlite3
import hashlib
import os
from datetime import datetime

from booking_rules import check_booking_rules


DATABASE_NAME = "smart_campus.db"


def get_connection():


    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        (
            campus_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            opening_time TEXT NOT NULL,
            closing_time TEXT NOT NULL,
            max_duration INTEGER NOT NULL
        )
    """)

    cursor.execute("""
         (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            campus_id INTEGER,
            FOREIGN KEY (campus_id) REFERENCES campuses(campus_id)
        )
    """)

    cursor.execute("""
         (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            campus_id INTEGER NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (campus_id) REFERENCES campuses(campus_id)
        )
    """)

    cursor.execute("""
         (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            campus_id INTEGER NOT NULL,
            booking_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (resource_id) REFERENCES resources(resource_id),
            FOREIGN KEY (campus_id) REFERENCES campuses(campus_id)
        )
    """)

    connection.commit()
    connection.close()


def add_campuses():


    connection = get_connection()
    cursor = connection.cursor()

    campuses = [
        ("Campus A", "08:00", "17:00", 2),
        ("Campus B", "08:00", "18:00", 3),
        ("Campus C", "09:00", "16:00", 1)
    ]

    for campus in campuses:
        cursor.execute("""
            INSERT OR IGNORE INTO campuses
            (name, opening_time, closing_time, max_duration)
            VALUES (?, ?, ?, ?)
        """, campus)

    connection.commit()
    connection.close()


def show_campuses():

    campuses = get_all_campuses()

    for campus in campuses:
        print(campus)


def get_all_campuses():


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM campuses ORDER BY campus_id")
    campuses = cursor.fetchall()

    connection.close()

    return campuses


def hash_password(password):


    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):


    try:
        salt, saved_password_hash = stored_hash.split(":")
        salt = bytes.fromhex(salt)

        entered_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return entered_hash.hex() == saved_password_hash

    except (ValueError, TypeError, AttributeError):
        return False


def register_user(full_name, username, password, role, campus_id=None):


    if not full_name.strip() or not username.strip() or not password:
        return False

    if role not in (
        "Lecturer",
        "Campus Administrator",
        "System Operator"
    ):
        return False

    if role != "System Operator" and campus_id is None:
        return False

    if role == "System Operator":
        campus_id = None

    password_hash = hash_password(password)
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (full_name, username, password_hash, role, campus_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name.strip(),
            username.strip(),
            password_hash,
            role,
            campus_id
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_user_by_username(username):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username.strip(),)
    )

    user = cursor.fetchone()
    connection.close()

    return user


def login_user(username, password):


    user = get_user_by_username(username)

    if user is None:
        return None

    stored_hash = user[3]

    if verify_password(password, stored_hash):
        return user

    return None


def add_resource(resource_code, name, resource_type, campus_id):


    if not resource_code.strip():
        return False

    if not name.strip() or not resource_type.strip():
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO resources
            (resource_code, name, resource_type, campus_id)
            VALUES (?, ?, ?, ?)
        """, (
            resource_code.strip(),
            name.strip(),
            resource_type.strip(),
            campus_id
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_resources_by_campus(campus_id):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM resources
        WHERE campus_id = ? AND active = 1
        ORDER BY resource_code
    """, (campus_id,))

    resources = cursor.fetchall()
    connection.close()

    return resources


def get_all_resources_by_campus(campus_id):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT resource_id, resource_code, name, resource_type, active
        FROM resources
        WHERE campus_id = ?
        ORDER BY resource_code
    """, (campus_id,))

    resources = cursor.fetchall()
    connection.close()

    return resources


def get_all_resources():


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            resources.resource_id,
            resources.resource_code,
            resources.name,
            resources.resource_type,
            campuses.name,
            resources.active
        FROM resources
        JOIN campuses
            ON resources.campus_id = campuses.campus_id
        ORDER BY campuses.name, resources.name
    """)

    resources = cursor.fetchall()
    connection.close()

    return resources


def set_resource_status(resource_id, campus_id, active):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE resources
        SET active = ?
        WHERE resource_id = ? AND campus_id = ?
    """, (int(bool(active)), resource_id, campus_id))

    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success


def add_booking(
    user_id,
    resource_id,
    campus_id,
    booking_date,
    start_time,
    duration
):



    try:
        duration = int(duration)

        if duration <= 0:
            return False

    except (ValueError, TypeError):
        return False


    try:
        booking_datetime = datetime.strptime(
            booking_date + " " + start_time,
            "%Y-%m-%d %H:%M"
        )
    except (ValueError, TypeError):
        return False


    if booking_datetime <= datetime.now():
        return False


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT campuses.name
        FROM resources
        JOIN campuses
            ON resources.campus_id = campuses.campus_id
        WHERE resources.resource_id = ?
          AND resources.campus_id = ?
          AND resources.active = 1
    """, (resource_id, campus_id))

    resource = cursor.fetchone()
    connection.close()

    if resource is None:
        print("Booking failed: Resource is unavailable.")
        return False

    campus_name = resource[0]


    valid, message = check_booking_rules(
        campus_name,
        start_time,
        duration
    )

    if not valid:
        print("Booking failed:", message)
        return False


    if has_booking_conflict(
        resource_id,
        booking_date,
        start_time,
        duration
    ):
        print("Booking failed: This resource is already booked.")
        return False


    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO bookings
            (user_id, resource_id, campus_id,
             booking_date, start_time, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            resource_id,
            campus_id,
            booking_date,
            start_time,
            duration
        ))

        connection.commit()
        print("Booking saved successfully!")
        return True

    except sqlite3.IntegrityError:
        print("Booking failed: Please check the account and resource.")
        return False

    finally:
        connection.close()



def get_user_bookings(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bookings.booking_id,
            bookings.user_id,
            bookings.resource_id,
            bookings.campus_id,
            bookings.booking_date,
            bookings.start_time,
            bookings.duration,
            bookings.status,
            resources.name,
            campuses.name
        FROM bookings
        JOIN resources
            ON bookings.resource_id = resources.resource_id
        JOIN campuses
            ON bookings.campus_id = campuses.campus_id
        WHERE bookings.user_id = ?
        ORDER BY bookings.booking_date DESC, bookings.start_time DESC
    """, (user_id,))

    bookings = cursor.fetchall()
    connection.close()
    return bookings



def has_booking_conflict(
    resource_id,
    booking_date,
    start_time,
    duration
):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT start_time, duration
        FROM bookings
        WHERE resource_id = ?
          AND booking_date = ?
          AND status = 'Active'
    """, (resource_id, booking_date))

    existing_bookings = cursor.fetchall()
    connection.close()

    new_start = int(start_time[:2]) * 60 + int(start_time[3:5])
    new_end = new_start + duration * 60

    for booking in existing_bookings:
        old_start = int(booking[0][:2]) * 60 + int(booking[0][3:5])
        old_end = old_start + booking[1] * 60

        if new_start < old_end and new_end > old_start:
            return True

    return False


def cancel_booking(booking_id, user_id):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT booking_date, start_time, status
        FROM bookings
        WHERE booking_id = ? AND user_id = ?
    """, (booking_id, user_id))

    booking = cursor.fetchone()

    if booking is None:
        connection.close()
        return False

    booking_date, start_time, status = booking

    if status != "Active":
        connection.close()
        return False

    try:
        booking_datetime = datetime.strptime(
            booking_date + " " + start_time,
            "%Y-%m-%d %H:%M"
        )
    except (ValueError, TypeError):
        connection.close()
        return False

    if booking_datetime <= datetime.now():
        connection.close()
        return False

    cursor.execute("""
        UPDATE bookings
        SET status = 'Cancelled'
        WHERE booking_id = ?
          AND user_id = ?
          AND status = 'Active'
    """, (booking_id, user_id))

    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success


def get_all_bookings():


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bookings.booking_id,
            users.full_name,
            resources.name,
            campuses.name,
            bookings.booking_date,
            bookings.start_time,
            bookings.duration,
            bookings.status
        FROM bookings
        JOIN users ON bookings.user_id = users.user_id
        JOIN resources ON bookings.resource_id = resources.resource_id
        JOIN campuses ON bookings.campus_id = campuses.campus_id
        ORDER BY bookings.booking_date, bookings.start_time
    """)

    bookings = cursor.fetchall()
    connection.close()

    return bookings


def get_bookings_by_campus(campus_id):


    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bookings.booking_id,
            users.full_name,
            resources.name,
            campuses.name,
            bookings.booking_date,
            bookings.start_time,
            bookings.duration,
            bookings.status
        FROM bookings
        JOIN users ON bookings.user_id = users.user_id
        JOIN resources ON bookings.resource_id = resources.resource_id
        JOIN campuses ON bookings.campus_id = campuses.campus_id
        WHERE bookings.campus_id = ?
        ORDER BY bookings.booking_date, bookings.start_time
    """, (campus_id,))

    bookings = cursor.fetchall()
    connection.close()

    return bookings


def get_most_used_resources():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            resources.name,
            campuses.name,
            COUNT(bookings.booking_id) AS booking_count
        FROM bookings
        JOIN resources
            ON bookings.resource_id = resources.resource_id
        JOIN campuses
            ON resources.campus_id = campuses.campus_id
        WHERE bookings.status = 'Active'
        GROUP BY resources.resource_id, resources.name, campuses.name
        ORDER BY booking_count DESC, resources.name
    """)

    resources = cursor.fetchall()
    connection.close()
    return resources


def get_average_booking_duration():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT AVG(duration)
        FROM bookings
        WHERE status = 'Active'
    """)

    result = cursor.fetchone()
    connection.close()

    if result[0] is None:
        return 0

    return round(result[0], 2)


if __name__ == "__main__":
    create_tables()
    add_campuses()
    show_campuses()
    print("Database setup completed!")
