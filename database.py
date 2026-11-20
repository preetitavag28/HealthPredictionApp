
import sqlite3

DB_NAME = "patients.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            dob TEXT,
            email TEXT,
            glucose REAL,
            haemoglobin REAL,
            cholesterol REAL,
            remarks TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks))

    conn.commit()
    conn.close()


def get_patients():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY id")
    records = cursor.fetchall()

    conn.close()
    return records


def update_patient(patient_id, name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET full_name=?, dob=?, email=?, glucose=?,
            haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id))

    conn.commit()
    conn.close()


def delete_patient(patient_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))

    conn.commit()
    conn.close()


def is_test_data_imported():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT setting_value FROM app_settings
        WHERE setting_key = 'employer_test_data_imported'
    """)

    result = cursor.fetchone()
    conn.close()

    return result is not None and result[0] == "yes"


def mark_test_data_imported():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO app_settings
        (setting_key, setting_value)
        VALUES ('employer_test_data_imported', 'yes')
    """)

    conn.commit()
    conn.close()
