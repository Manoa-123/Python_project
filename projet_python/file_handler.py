import json
import os

ATTENDANCE_FILE = "attendance_records.txt"

def load_records():
    """Load attendance records from file."""
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_records(records):
    """Save attendance records to file."""
    with open(ATTENDANCE_FILE, 'w') as file:
        json.dump(records, file, indent=1,ensure_ascii=False)

def load_employees():
    """Charge la liste des ID d'employés uniques depuis les enregistrements de présence."""
    records = load_records()
    # Extraction des ID d'employés uniques
    employee_ids = list({record['employee_id'] for record in records})
    return employee_ids
