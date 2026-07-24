import json


class Person:
    def __init__(self, name, age, contact):
        self.__name = name
        self.__age = age
        self.__contact = contact

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def contact(self):
        return self.__contact


class Patient(Person):
    def __init__(self, name, age, contact, patient_id, medical_history):
        super().__init__(name, age, contact)
        self.__patient_id = patient_id
        self.__medical_history = medical_history if medical_history is not None else []

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def medical_history(self):
        return self.__medical_history

    def add_history(self, note):
        self.__medical_history.append(note)
        return "Sucessfully added to the history"

    def get_summary(self):
        return f"Patient Name: {self.name} \nPatient Age: {self.age} \nPatient contact: {self.contact} \nPatient: {self.patient_id}"

    def to_dict(self):
        return {
            "patient_name": self.name,
            "patient_age": self.age,
            "patient_contact": self.contact,
            "patient_id": self.patient_id,
            "patient_medical_history": self.medical_history,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["patient_name"],
            data["patient_age"],
            data["patient_contact"],
            data["patient_id"],
            data["patient_medical_history"],
        )


class Doctor(Person):
    def __init__(self, name, age, contact, doctor_id, specialization, available_days):
        super().__init__(name, age, contact)
        self.__doctor_id = doctor_id
        self.__specialization = specialization
        self.__doctor_available_days = [day.lower() for day in available_days]

    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def specialization(self):
        return self.__specialization

    @property
    def available_days(self):
        return self.__doctor_available_days

    def is_available(self, day):
        if day.strip().lower() not in self.available_days:
            return False
        else:
            return True

    def get_summary(self):
        return f"Doctor Name: {self.name} \nDoctor Age: {self.age} \nDoctor contact: {self.contact} \nDoctor_id: {self.doctor_id} \nDoctor Specialisation: {self.specialization} \nAvailable days: {self.available_days}"

    def to_dict(self):
        return {
            "doctor_name": self.name,
            "doctor_age": self.age,
            "doctor_contact": self.contact,
            "doctor_id": self.doctor_id,
            "doctor_specialization": self.specialization,
            "doctor_available_days": self.available_days,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["doctor_name"],
            data["doctor_age"],
            data["doctor_contact"],
            data["doctor_id"],
            data["doctor_specialization"],
            data["doctor_available_days"],
        )


class Appointment:
    def __init__(self, patient_id, doctor_id, date, status, appointment_id):
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__date = date
        self.__status = status
        self.__appointment_id = appointment_id

    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, new_patient_id):
        self.__patient_id = new_patient_id

    @property
    def doctor_id(self):
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, new_doctor_id):
        self.__doctor_id = new_doctor_id

    @property
    def date(self):
        return self.__date

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        if new_status not in ["scheduled", "cancelled", "completed"]:
            raise ValueError(f"Invalid status: {new_status}")
        self.__status = new_status

    @property
    def appointment_id(self):
        return self.__appointment_id

    @date.setter
    def date(self, new_date):
        self.__date = new_date

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "status": self.status,
            "appointment_id": self.appointment_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["patient_id"],
            data["doctor_id"],
            data["date"],
            data["status"],
            data["appointment_id"],
        )

    def get_summary(self):
        return f"Appointment ID: {self.appointment_id} \nAppointment on {self.date} \nDoctor ID: {self.doctor_id} \nPatient ID: {self.patient_id} \nStatus: {self.status}"
