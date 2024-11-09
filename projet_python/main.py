import customtkinter as ctk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime
from attendance import mark_attendance, view_records, search_employee, generate_summary
from file_handler import load_employees

def gui_mark_attendance():
    """Interface pour marquer la présence avec un sélecteur de date et un menu déroulant pour le statut."""
    dialog = ctk.CTkToplevel()
    dialog.title("Marquer la présence")
    dialog.geometry("500x500")
    
    # Rendre la fenêtre modale
    dialog.transient(dialog.master)
    dialog.grab_set()
    
    # Charger les ID d'employés depuis les enregistrements
    employees = load_employees()
    
    # Variables pour l'ID de l'employé et le statut
    employee_id = ctk.StringVar()
    status = ctk.StringVar(value="Present")
    
    # Frame pour la sélection/saisie de l'ID employé
    id_frame = ctk.CTkFrame(dialog)
    id_frame.pack(pady=5, padx=10, fill="x")
    
    ctk.CTkLabel(id_frame, text="ID employé (numérique):").pack(pady=5)
    
    # Menu déroulant pour sélectionner un ID existant
    display_employees = [eid[1:].lstrip('0') for eid in employees]
    id_menu = ctk.CTkOptionMenu(id_frame, variable=employee_id, values=display_employees)
    id_menu.pack(pady=5)
    
    ctk.CTkLabel(id_frame, text="OU").pack(pady=2)
    
    id_entry = ctk.CTkEntry(id_frame)
    id_entry.pack(pady=5)
    
    def validate_and_format_id(id_str):
        """Valide et formate l'ID employé."""
        if not id_str.isdigit():
            messagebox.showerror("Erreur", "L'ID employé doit être numérique.")
            return None
            
        formatted_id = f"E{int(id_str):03}"
        return formatted_id
    
    def update_employee_id():
        """Ajoute l'employé saisi à la liste si ce n'est pas déjà présent."""
        new_id = id_entry.get().strip()
        
        formatted_id = validate_and_format_id(new_id)
        if not formatted_id:
            id_entry.delete(0, 'end')
            return
            
        if formatted_id not in employees:
            employees.append(formatted_id)
            display_employees = [eid[1:].lstrip('0') for eid in employees]
            id_menu.configure(values=display_employees)
            employee_id.set(new_id)
            id_entry.delete(0, 'end')
            messagebox.showinfo("Succès", f"Nouvel employé {formatted_id} ajouté.")
        else:
            messagebox.showwarning("Attention", "Cet ID employé existe déjà.")
            id_entry.delete(0, 'end')
    
    ctk.CTkButton(id_frame, text="Ajouter nouvel ID", command=update_employee_id).pack(pady=5)
    
    # Sélection de la date
    ctk.CTkLabel(dialog, text="Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = DateEntry(dialog, width=12, background='darkblue', foreground='white', 
                          borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry.pack(pady=5)
    
     # Sélection du statut de présence
    ctk.CTkLabel(dialog, text="Statut:").pack(pady=5)
    status_menu = ctk.CTkOptionMenu(dialog, values=["Present", "Absent"], variable=status)
    status_menu.pack(pady=5)
    
    def submit():
        """Enregistre la présence de l'employé sélectionné ou saisi."""
        if id_entry.get().strip():
            raw_id = id_entry.get().strip()
            formatted_id = validate_and_format_id(raw_id)
            if not formatted_id:
                return
        else:
            raw_id = employee_id.get().strip()
            formatted_id = f"E{int(raw_id):03}"
            
        date = date_entry.get()
        result = mark_attendance(formatted_id, date, status.get())
        messagebox.showinfo("Résultat", result)
        dialog.destroy()
    
     # Boutons pour enregistrer ou annuler
    buttons_frame = ctk.CTkFrame(dialog)
    buttons_frame.pack(pady=10, fill="x", padx=20)
    
    ctk.CTkButton(buttons_frame, text="Enregistrer", command=submit, 
                  fg_color="green", hover_color="dark green").pack(side="left", expand=True, padx=5)
    ctk.CTkButton(buttons_frame, text="Annuler", command=dialog.destroy,
                  fg_color="red", hover_color="dark red").pack(side="left", expand=True, padx=5)
    
    # Attendre que la fenêtre soit fermée
    dialog.wait_window()

def gui_view_records():
    """Interface pour afficher les enregistrements."""
    dialog = ctk.CTkToplevel()
    dialog.title("Afficher les enregistrements")
    dialog.geometry("600x400")
    
    # Rendre la fenêtre modale
    dialog.transient(dialog.master)
    dialog.grab_set()
    
    records = view_records()
    
    # Créer un widget Text pour afficher les enregistrements
    text_widget = ctk.CTkTextbox(dialog, width=550, height=300)
    text_widget.pack(pady=20, padx=20)
    
    if isinstance(records, str):
        text_widget.insert("1.0", records)
    else:
        record_list = "\n".join([f"ID: {rec['employee_id']}, Date: {rec['date']}, Statut: {rec['status']}" 
                                for rec in records])
        text_widget.insert("1.0", record_list)
    
    text_widget.configure(state="disabled")  # Rendre le texte en lecture seule
    
    # Bouton Fermer
    ctk.CTkButton(dialog, text="Fermer", command=dialog.destroy,
                  fg_color="red", hover_color="dark red").pack(pady=10)
    
    # Attendre que la fenêtre soit fermée
    dialog.wait_window()

def gui_search_employee():
    """Interface pour rechercher la présence d'un employé avec saisie numérique."""
    search_dialog = ctk.CTkToplevel()
    search_dialog.title("Rechercher la présence")
    search_dialog.geometry("500x200")
    
    # Rendre la fenêtre modale
    search_dialog.transient(search_dialog.master)
    search_dialog.grab_set()
    
    search_frame = ctk.CTkFrame(search_dialog)
    search_frame.pack(pady=10, padx=10, fill="x")
    
    ctk.CTkLabel(search_frame, text="Entrer l'ID employé (numérique):").pack(pady=5)
    
    id_entry = ctk.CTkEntry(search_frame)
    id_entry.pack(pady=5)
    
    def search():
        """Recherche les enregistrements de présence pour un ID employé donné."""
        raw_id = id_entry.get().strip()
        
        if not raw_id:
            messagebox.showerror("Erreur", "Veuillez entrer un ID d'employé.")
            return
            
        if not raw_id.isdigit():
            messagebox.showerror("Erreur", "L'ID employé doit être numérique.")
            return
            
        formatted_id = f"E{int(raw_id):03}"
        
        employee_records = search_employee(formatted_id)
        
        # Créer une nouvelle fenêtre pour afficher les résultats
        results_dialog = ctk.CTkToplevel(search_dialog)
        results_dialog.title("Résultats de la recherche")
        results_dialog.geometry("500x300")
        
        # Rendre la fenêtre de résultats modale
        results_dialog.transient(search_dialog)
        results_dialog.grab_set()
        
        text_widget = ctk.CTkTextbox(results_dialog, width=450, height=200)
        text_widget.pack(pady=20, padx=20)
        
        if isinstance(employee_records, str):
            text_widget.insert("1.0", employee_records)
        else:
            records = "\n".join([f"Date: {rec['date']}, Statut: {rec['status']}" 
                               for rec in employee_records])
            text_widget.insert("1.0", f"Enregistrements pour l'employé {formatted_id}:\n\n{records}")
        
        text_widget.configure(state="disabled")
        
        ctk.CTkButton(results_dialog, text="Fermer", command=results_dialog.destroy,
                      fg_color="red", hover_color="dark red").pack(pady=10)
        
        # Attendre que la fenêtre de résultats soit fermée
        results_dialog.wait_window()
        
    buttons_frame = ctk.CTkFrame(search_dialog)
    buttons_frame.pack(pady=10, fill="x", padx=20)
    
    ctk.CTkButton(buttons_frame, text="Rechercher", command=search,
                  fg_color="green", hover_color="dark green").pack(side="left", expand=True, padx=5)
    ctk.CTkButton(buttons_frame, text="Annuler", command=search_dialog.destroy,
                  fg_color="red", hover_color="dark red").pack(side="left", expand=True, padx=5)
    
    # Attendre que la fenêtre de recherche soit fermée
    search_dialog.wait_window()

def gui_generate_summary():
    """Interface pour générer le résumé de présence."""
    summary_dialog = ctk.CTkToplevel()
    summary_dialog.title("Résumé de la présence")
    summary_dialog.geometry("600x400")
    
    # Rendre la fenêtre modale
    summary_dialog.transient(summary_dialog.master)
    summary_dialog.grab_set()
    
    text_widget = ctk.CTkTextbox(summary_dialog, width=550, height=300)
    text_widget.pack(pady=20, padx=20)
    
    summary = generate_summary()
    if summary:
        summary_list = "\n".join([
            f"ID: {emp}, Present: {stats['present']} jours, "
            f"Absent: {stats['absent']} jours, "
            f"Pourcentage: {stats['pourcentage']:.2f}%"
            for emp, stats in summary.items()
        ])
        text_widget.insert("1.0", summary_list)
    else:
        text_widget.insert("1.0", "Aucun enregistrement trouvé.")
    
    text_widget.configure(state="disabled")
    
    ctk.CTkButton(summary_dialog, text="Fermer", command=summary_dialog.destroy,
                  fg_color="red", hover_color="dark red").pack(pady=10)
    
    # Attendre que la fenêtre soit fermée
    summary_dialog.wait_window()

# changer de mode
def toggle_appearance_mode():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        mode_switch.configure(text="Mode Sombre")
    else:
        ctk.set_appearance_mode("Dark")
        mode_switch.configure(text="Mode Clair")

#Affichage de l'interface principale
def display_interface():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("Système de gestion des présences des employés")
    window.geometry("400x400")

#Message de confirmation pour quitter
    def confirm_quit():
        """Affiche une boîte de dialogue de confirmation avant de quitter."""
        if messagebox.askokcancel("Confirmation", 
            "Êtes-vous sûr de vouloir quitter l'application ?"):
            window.quit()

    window.protocol("WM_DELETE_WINDOW", confirm_quit)

    title_label = ctk.CTkLabel(window, text="Système de gestion des présences", 
                              font=("Helvetica", 20, "bold"))
    title_label.pack(pady=20)

    global mode_switch
    mode_switch = ctk.CTkSwitch(window, text="Mode Sombre", command=toggle_appearance_mode)
    mode_switch.pack(pady=10)
    mode_switch.select()

    mark_button = ctk.CTkButton(window, text="Marquer la présence", command=gui_mark_attendance)
    mark_button.pack(pady=10)

    view_button = ctk.CTkButton(window, text="Afficher les enregistrements", command=gui_view_records)
    view_button.pack(pady=10)

    search_button = ctk.CTkButton(window, text="Rechercher la présence d'un employé", 
                                 command=gui_search_employee)
    search_button.pack(pady=10)

    summary_button = ctk.CTkButton(window, text="Générer un résumé", command=gui_generate_summary)
    summary_button.pack(pady=10)

    quit_button = ctk.CTkButton(window, text="Quitter", command=confirm_quit, 
                               fg_color="#f44336", hover_color="#e53935")
    quit_button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    display_interface()