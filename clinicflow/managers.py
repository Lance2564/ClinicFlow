import json
import os
from clinicflow import models as m
from datetime import datetime


class PatientManager:
    def __init__(self):
        self.__patient_dict = {}
        self.__filepath = "data/patients.json"
        self.load_from_json()

    @property
    def patient_dict(self):
        return self.__patient_dict

    @property
    def filepath(self):
        return self.__filepath

    def add_patient(self, name, age, contact, patient_id, medical_history):
        new_patient = m.Patient(name, age, contact, patient_id, medical_history)
        self.patient_dict[patient_id] = new_patient
        self.save_to_json()

    def remove_patient(self, patient_id):
        if patient_id in self.patient_dict:
            del self.patient_dict[patient_id]
            self.save_to_json()
            return True
        else:
            return False

    def get_patient(self, patient_id):
        return self.patient_dict.get(patient_id)

    def find_patient(self, name):
        results = []
        for patient in self.patient_dict.values():
            if patient.name.strip().lower() == name.strip().lower():
                results.append(patient)
        return results

    def save_to_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        raw_data = {
            pid: patient.to_dict() for pid, patient in self.patient_dict.items()
        }
        with open(self.filepath, "w") as file:
            json.dump(raw_data, file, indent=4)

    def load_from_json(self):
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r") as file:
                raw_data = json.load(file)

            self.__patient_dict = {}
            for pid, info in raw_data.items():
                self.__patient_dict[pid] = m.Patient.from_dict(info)

            print(f"Database loaded. {len(self.patient_dict)} profiles active.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to read database file due to format issues: {e}")

    def wipe(self):
        self.__patient_dict.clear()
        self.save_to_json()


class DoctorManager:
    def __init__(self):
        self.__doctor_dict = {}
        self.__filepath = "data/doctors.json"
        self.load_from_json()

    @property
    def doctor_dict(self):
        return self.__doctor_dict

    @property
    def filepath(self):
        return self.__filepath

    def add_doctor(self, name, age, contact, doctor_id, specialization, available_days):
        new_doctor = m.Doctor(
            name, age, contact, doctor_id, specialization, available_days
        )
        self.__doctor_dict[doctor_id] = new_doctor
        self.save_to_json()

    def remove_doctor(self, doctor_id):
        if doctor_id in self.doctor_dict:
            del self.doctor_dict[doctor_id]
            self.save_to_json()
            return True
        else:
            return False

    def get_doctor(self, doctor_id):
        return self.doctor_dict.get(doctor_id)

    def save_to_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        raw_data = {
            doc_id: doctor.to_dict() for doc_id, doctor in self.doctor_dict.items()
        }
        with open(self.filepath, "w") as file:
            json.dump(raw_data, file, indent=4)

    def load_from_json(self):
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r") as file:
                raw_data = json.load(file)

            self.__doctor_dict = {}
            for doc_id, info in raw_data.items():
                self.__doctor_dict[doc_id] = m.Doctor.from_dict(info)

            print(f"Database loaded. {len(self.doctor_dict)} doctor profiles active.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to read database file due to format issues: {e}")

    def wipe(self):
        self.__doctor_dict.clear()
        self.save_to_json()


class AppointmentManager:
    def __init__(self, patient_manager, doctor_manager):
        self.__appointments = {}
        self.__filepath = "data/appointments.json"
        self.__patient_manager = patient_manager
        self.__doctor_manager = doctor_manager
        self.load_from_json()

    @property
    def appointments(self):
        return self.__appointments

    @property
    def filepath(self):
        return self.__filepath

    @property
    def patient_manager(self):
        return self.__patient_manager

    @property
    def doctor_manager(self):
        return self.__doctor_manager

    def book_appointment(self, patient_id, doctor_id, date):
        patient = self.patient_manager.get_patient(patient_id)
        if patient is None:
            print(
                "No such patient found. This may have occurred due to: \nWrong Patient id \nThe patient doesn't exist"
            )
            return

        doctor = self.doctor_manager.get_doctor(doctor_id)
        if doctor is None:
            print(
                "No such Doctor found. This may have occurred due to: \nWrong Doctor id \nThe doctor doesn't exist"
            )
            return

        day = datetime.strptime(date, "%Y-%m-%d").strftime("%A").lower()
        if not doctor.is_available(day):
            print(
                f"Doctor {doctor_id} is not available on {day.capitalize()}. Available days: {doctor.available_days}"
            )
            return

        for appointment in self.__appointments.values():
            if (
                appointment.doctor_id == doctor_id
                and appointment.date == date
                and appointment.status == "scheduled"
            ):
                print(f"Doctor {doctor_id} already has an appointment on {date}.")
                return

        appointment_id = f"A{len(self.__appointments) + 1:03d}"

        new_appointment = m.Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            status="scheduled",
            appointment_id=appointment_id,
        )

        self.__appointments[appointment_id] = new_appointment
        self.save_to_json()
        print(f"Appointment {appointment_id} successfully booked for {date}.")

    def cancel_appointment(self, appointment_id):
        if appointment_id in self.__appointments:
            self.__appointments[appointment_id].status = "cancelled"
            self.save_to_json()
            print(f"Appointment {appointment_id} successfully cancelled.")
        else:
            print(f"No appointment with ID {appointment_id} found.")

    def complete_appointment(self, appointment_id):
        if appointment_id in self.__appointments:
            self.__appointments[appointment_id].status = "completed"
            self.save_to_json()
            print("The appointment status has been turned to completed")
        else:
            print(f"No appointment with the id {appointment_id} was found.")

    def get_patient_appointments(self, patient_id):
        results = []
        for appointment in self.__appointments.values():
            if appointment.patient_id == patient_id:
                results.append(appointment.get_summary())
        if not results:
            print(f"No appointments found for patient {patient_id}.")
        return results

    def get_doctor_schedule(self, doctor_id, date):
        results = []
        for appointment in self.__appointments.values():
            if (
                appointment.doctor_id == doctor_id
                and appointment.date == date
                and appointment.status != "cancelled"
            ):
                results.append(appointment.get_summary())
        if not results:
            print(f"No active schedule found for doctor {doctor_id}.")
        return results

    def reschedule_appointment(self, appointment_id, new_date):
        if appointment_id not in self.__appointments:
            return "No appointment with that ID."

        appointment = self.__appointments[appointment_id]
        if appointment.status != "scheduled":
            return f"Cannot reschedule — appointment is '{appointment.status}'."

        doctor = self.doctor_manager.get_doctor(appointment.doctor_id)
        if doctor is None:
            return "The doctor for this appointment no longer exists."

        day = datetime.strptime(new_date, "%Y-%m-%d").strftime("%A").lower()
        if not doctor.is_available(day):
            return f"Doctor is not available on {day.capitalize()}."

        for other in self.__appointments.values():
            if (
                other.appointment_id != appointment_id
                and other.doctor_id == appointment.doctor_id
                and other.date == new_date
                and other.status == "scheduled"
            ):
                return "Doctor already has an appointment on that date."

        appointment.date = new_date
        self.save_to_json()
        return None

    def save_to_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        raw_data = {aid: app.to_dict() for aid, app in self.__appointments.items()}
        with open(self.filepath, "w") as file:
            json.dump(raw_data, file, indent=4)

    def load_from_json(self):
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r") as file:
                raw_data = json.load(file)

            self.__appointments = {}
            for aid, info in raw_data.items():
                self.__appointments[aid] = m.Appointment.from_dict(info)
            print(
                f"Database loaded. {len(self.__appointments)} active appointments processed."
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to read database file due to format issues: {e}")

    def wipe(self):
        self.__appointments.clear()
        self.save_to_json()
