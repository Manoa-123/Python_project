from file_handler import load_records, save_records , load_employees
from datetime import datetime

def mark_attendance(employee_id, date, status):
    """Enregistrer la présence d'un employé avec vérification des entrées via une boucle while."""
    records = load_records()
    employees = load_employees()  # Charge la liste des employés connus

    # Vérification de la validité du statut en utilisant une boucle while
    while status not in ["Present", "Absent"]:
        print("Statut invalide. Veuillez entrer 'Present' ou 'Absent'.")
        status = input("Entrez le statut (Present/Absent) : ")

    # Vérification du format de date en utilisant une boucle while
    while True:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break  # Sortie de la boucle si la date est valide
        except ValueError:
            print("Format de date invalide. Veuillez utiliser AAAA-MM-JJ.")
            date = input("Entrez la date (AAAA-MM-JJ) : ")

    # Vérifie si la présence a déjà été enregistrée pour cet employé à cette date
    for record in records:
        if record["employee_id"] == employee_id and record["date"] == date:
            return "La présence de cet employé a déjà été enregistrée pour cette date."

    # Si non, ajoute l'enregistrement de présence
    records.append({"employee_id": employee_id, "date": date, "status": status})
    save_records(records)
    return "Présence enregistrée avec succès."

def view_records():
    """Voir tous les enregistrements."""
    records = load_records()
    return records if records else "Pas d'enregistrement retrouvé."

def search_employee(formatted_id):
    """Rechercher les enregistrements de présence pour un employé spécifique."""
    records = load_records()
    employee_records = [record for record in records if record['employee_id'] == formatted_id]
    return employee_records if employee_records else f"Aucun enregistrement trouvé pour l'ID employé : {formatted_id}"

def generate_summary():
    """Générer un résumé des présences pour tous les employés."""
    records = load_records()
    summary = {}
    
    for record in records:
        employee_id = record['employee_id']
        if employee_id not in summary:
            summary[employee_id] = {"present": 0, "absent": 0, "total": 0}
        
        summary[employee_id][record['status'].lower()] += 1
        summary[employee_id]['total'] += 1
    
    for employee_id, stats in summary.items():
        present_percentage = (stats['present'] / stats['total']) * 100
        stats['pourcentage'] = present_percentage
    
    return summary

