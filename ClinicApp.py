class Patient:

    def __init__(self, patient_id, name, condition):
        self.patient_id = patient_id
        self.name = name
        self.condition = condition

class Doctor:
    def __init__(self, doctor_id, name):
        self.doctor_id = doctor_id
        self.name = name
        self.patients = []  # To hold Patient objects

    def add_patient(self, patient):
        if len(self.patients) < 16:
            self.patients.append(patient)
            print(f"{patient.name} added to {self.name}'s schedule.")
            return True
        else:
            print(f"{self.name} is already scheduled with 16 patients.")
            return False

    def remove_patient(self, patient_id):
        for patient in self.patients:
            if patient.patient_id == patient_id:
                self.patients.remove(patient)
                print(f"Patient with ID {patient_id} removed from {self.name}'s schedule.")
                return True
        print(f"Patient with ID {patient_id} not found in {self.name}'s schedule.")
        return False

    def list_patients(self):
        print(f"Patients for Dr. {self.name}:")
        if not self.patients:
            print("No patients scheduled.")
        else:
            for patient in self.patients:
                print(f"- ID: {patient.patient_id}, Name: {patient.name}, Condition: {patient.condition}")

# Example usage:
doc1 = Doctor(1, "Smith")
pat1 = Patient(101, "Alice", "Fever")
pat2 = Patient(102, "Bob", "Headache")

doc1.add_patient(pat1)
doc1.add_patient(pat2)
doc1.list_patients()

doc1.remove_patient(101)
doc1.list_patients()

import sqlite3

def create_database():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    # Create doctor table
    c.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    # Create patient table
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT,
            condition TEXT
        )
    ''')

    # Create schedule table (to link doctors and patients)
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            patient_id INTEGER,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_doctor_db(doctor_id, name):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO doctors (doctor_id, name) VALUES (?, ?)", (doctor_id, name))
        conn.commit()
        print(f"Doctor {name} added to database.")
    except sqlite3.IntegrityError:
        print(f"Doctor with ID {doctor_id} already exists.")
    conn.close()

def add_patient_db(patient_id, name, condition):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO patients (patient_id, name, condition) VALUES (?, ?, ?)", (patient_id, name, condition))
        conn.commit()
        print(f"Patient {name} added to database.")
    except sqlite3.IntegrityError:
        print(f"Patient with ID {patient_id} already exists.")
    conn.close()

def schedule_appointment_db(doctor_id, patient_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    # Check if doctor has reached the 16-patient limit
    c.execute("SELECT COUNT(*) FROM schedule WHERE doctor_id = ?", (doctor_id,))
    count = c.fetchone()[0]

    if count < 16:
        try:
            c.execute("INSERT INTO schedule (doctor_id, patient_id) VALUES (?, ?)", (doctor_id, patient_id))
            conn.commit()
            print(f"Appointment scheduled for doctor {doctor_id} and patient {patient_id}.")
        except sqlite3.IntegrityError:
            print(f"Patient {patient_id} already scheduled with doctor {doctor_id}.")
    else:
        print(f"Doctor {doctor_id} is already scheduled with 16 patients.")

    conn.close()

# Example usage:
create_database()
add_doctor_db(1, "Smith")
add_patient_db(101, "Alice", "Fever")
add_patient_db(102, "Bob", "Headache")
#schedule_appointment_db(1, 101)
 #schedule_appointment_db(1, 102)

import tkinter as tk
from tkinter import messagebox


# (Include the database functions from step 3 here)
# (Include the database functions from step 3 here)
# (Include the Patient and Doctor class definitions from step 1 here)

class ClinicApp:
    def __init__(self, master):
        self.master = master
        master.title("Clinic Scheduling")

        # --- Doctor Section ---
        self.doctor_frame = tk.LabelFrame(master, text="Doctor Management")
        self.doctor_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.doctor_frame, text="Doctor ID:").grid(row=0, column=0)
        self.doctor_id_entry = tk.Entry(self.doctor_frame)
        self.doctor_id_entry.grid(row=0, column=1)

        tk.Label(self.doctor_frame, text="Doctor Name:").grid(row=1, column=0)
        self.doctor_name_entry = tk.Entry(self.doctor_frame)
        self.doctor_name_entry.grid(row=1, column=1)

        self.add_doctor_button = tk.Button(self.doctor_frame, text="Add Doctor", command=self.add_doctor_gui)
        self.add_doctor_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Add button to view all doctors
        self.view_doctors_button = tk.Button(self.doctor_frame, text="View All Doctors", command=self.view_all_doctors_gui)
        self.view_doctors_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.view_free_doctors_button = tk.Button(self.doctor_frame, text="View Free Doctors", command=self.view_free_doctors_gui)
        self.view_free_doctors_button.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Patient Section ---
        self.patient_frame = tk.LabelFrame(master, text="Patient Management")
        self.patient_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.patient_frame, text="Patient ID:").grid(row=0, column=0)
        self.patient_id_entry = tk.Entry(self.patient_frame)
        self.patient_id_entry.grid(row=0, column=1)

        tk.Label(self.patient_frame, text="Patient Name:").grid(row=1, column=0)
        self.patient_name_entry = tk.Entry(self.patient_frame)
        self.patient_name_entry.grid(row=1, column=1)

        tk.Label(self.patient_frame, text="Condition:").grid(row=2, column=0)
        self.condition_entry = tk.Entry(self.patient_frame)
        self.condition_entry.grid(row=2, column=1)

        self.add_patient_button = tk.Button(self.patient_frame, text="Add Patient", command=self.add_patient_gui)
        self.add_patient_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Add button to view all patients
        self.view_patients_button = tk.Button(self.patient_frame, text="View All Patients", command=self.view_all_patients_gui)
        self.view_patients_button.grid(row=4, column=0, columnspan=2, pady=5)


        # --- Scheduling Section ---
        self.schedule_frame = tk.LabelFrame(master, text="Scheduling")
        self.schedule_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.schedule_frame, text="Doctor ID:").grid(row=0, column=0)
        self.schedule_doctor_id_entry = tk.Entry(self.schedule_frame)
        self.schedule_doctor_id_entry.grid(row=0, column=1)

        tk.Label(self.schedule_frame, text="Patient ID:").grid(row=1, column=0)
        self.schedule_patient_id_entry = tk.Entry(self.schedule_frame)
        self.schedule_patient_id_entry.grid(row=1, column=1)

        self.schedule_button = tk.Button(self.schedule_frame, text="Schedule Appointment", command=self.schedule_appointment_gui)
        self.schedule_button.grid(row=2, column=0, columnspan=2, pady=5)

        # --- View Schedule Section (Example - you can make this more detailed) ---
        self.view_schedule_button = tk.Button(master, text="View Doctor's Schedule (by ID)", command=self.view_schedule_gui)
        self.view_schedule_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.view_schedule_doctor_id_entry = tk.Entry(master)
        self.view_schedule_doctor_id_entry.grid(row=3, column=0, columnspan=2)

    # (Include the add_doctor_gui, add_patient_gui, schedule_appointment_gui, and view_schedule_gui methods here)

    def add_doctor_gui(self):
        doctor_id = self.doctor_id_entry.get()
        name = self.doctor_name_entry.get()
        if doctor_id and name:
            add_doctor_db(int(doctor_id), name)
            self.doctor_id_entry.delete(0, tk.END)
            self.doctor_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both Doctor ID and Name.")

    def add_patient_gui(self):
        patient_id = self.patient_id_entry.get()
        name = self.patient_name_entry.get()
        condition = self.condition_entry.get()
        if patient_id and name and condition:
            add_patient_db(int(patient_id), name, condition)
            self.patient_id_entry.delete(0, tk.END)
            self.patient_name_entry.delete(0, tk.END)
            self.condition_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter Patient ID, Name, and Condition.")

    def schedule_appointment_gui(self):
        doctor_id = self.schedule_doctor_id_entry.get()
        patient_id = self.schedule_patient_id_entry.get()
        if doctor_id and patient_id:
            schedule_appointment_db(int(doctor_id), int(patient_id))
            self.schedule_doctor_id_entry.delete(0, tk.END)
            self.schedule_patient_id_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both Doctor ID and Patient ID for scheduling.")

    def view_schedule_gui(self):
        doctor_id = self.view_schedule_doctor_id_entry.get()
        if doctor_id:
            conn = sqlite3.connect('clinic.db')
            c = conn.cursor()
            c.execute("""
                SELECT p.name, p.condition
                FROM patients p
                JOIN schedule s ON p.patient_id = s.patient_id
                WHERE s.doctor_id = ?
            """, (int(doctor_id),))
            schedule_data = c.fetchall()
            conn.close()

            if schedule_data:
                schedule_text = f"Schedule for Doctor {doctor_id}:\n"
                for patient_name, patient_condition in schedule_data:
                    schedule_text += f"- Patient: {patient_name}, Condition: {patient_condition}\n"
                messagebox.showinfo("Doctor's Schedule", schedule_text)
            else:
                messagebox.showinfo("Doctor's Schedule", f"No patients scheduled for Doctor {doctor_id}.")
        else:
            messagebox.showwarning("Input Error", "Please enter a Doctor ID to view the schedule.")

    def view_all_doctors_gui(self):
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT doctor_id, name FROM doctors")
        doctors_data = c.fetchall()
        conn.close()

        if doctors_data:
            doctors_text = "All Doctors:\n"
            for doctor_id, doctor_name in doctors_data:
                doctors_text += f"- ID: {doctor_id}, Name: {doctor_name}\n"
            messagebox.showinfo("All Doctors", doctors_text)
        else:
            messagebox.showinfo("All Doctors", "No doctors found in the database.")

    def view_all_patients_gui(self):
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT patient_id, name, condition FROM patients")
        patients_data = c.fetchall()
        conn.close()

        if patients_data:
            patients_text = "All Patients:\n"
            for patient_id, patient_name, patient_condition in patients_data:
                patients_text += f"- ID: {patient_id}, Name: {patient_name}, Condition: {patient_condition}\n"
            messagebox.showinfo("All Patients", patients_text)
        else:
            messagebox.showinfo("All Patients", "No patients found in the database.")

    def view_free_doctors_gui(self):
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()

        # SQL query to find doctors with less than 16 scheduled patients
        # We use a LEFT JOIN to include doctors with no appointments
        c.execute("""
            SELECT d.doctor_id, d.name
            FROM doctors d
            LEFT JOIN schedule s ON d.doctor_id = s.doctor_id
            GROUP BY d.doctor_id, d.name
            HAVING COUNT(s.patient_id) < 16
        """)
        free_doctors_data = c.fetchall()
        conn.close()

        if free_doctors_data:
            free_doctors_text = "Free Doctors (less than 16 appointments):\n"
            for doctor_id, doctor_name in free_doctors_data:
                free_doctors_text += f"- ID: {doctor_id}, Name: {doctor_name}\n"
            messagebox.showinfo("Free Doctors", free_doctors_text)
        else:
            messagebox.showinfo("Free Doctors", "No doctors are currently free.")


# Create the database file if it doesn't exist
create_database()

root = tk.Tk()
app = ClinicApp(root)
root.mainloop()

# Create the database file if it doesn't exist
create_database()
if __name__ == '__main__':
  try:
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()
  except Exception as e:
    print(f"An error occurred: {e}")