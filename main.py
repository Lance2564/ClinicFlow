import tkinter as tk
from clinicflow import managers as ma

BG = "#1e1e1e"
PANEL_BG = "#2a2a2a"
FG = "#e0e0e0"
MUTED_FG = "#9a9a9a"
ACCENT = "#4da3ff"

BASE_MENU_FONT_SIZE = 22
BASE_LABEL_FONT_SIZE = 15
BASE_INPUT_FONT_SIZE = 18
BASE_BUTTON_FONT_SIZE = 16
BASE_TITLE_FONT_SIZE = 30


def scale_factor(window):
    window.update_idletasks()
    screen_h = window.winfo_screenheight()
    factor = screen_h / 1080
    return max(0.75, min(factor, 1.75))


def make_label(parent, text, size, bold=False, muted=False, **kwargs):
    weight = "bold" if bold else "normal"
    return tk.Label(
        parent,
        text=text,
        font=("Helvetica", size, weight),
        bg=kwargs.pop("bg", PANEL_BG if isinstance(parent, tk.Toplevel) else BG),
        fg=MUTED_FG if muted else FG,
        **kwargs,
    )


def make_entry(parent, font_size, width=28):
    return tk.Entry(
        parent,
        bg="#333333",
        fg="white",
        insertbackground="white",
        font=("Helvetica", font_size),
        justify="center",
        width=width,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#444444",
    )


def make_button(parent, text, command, font_size):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica", font_size, "bold"),
        bg=ACCENT,
        fg="#1e1e1e",
        activebackground="#3d82cc",
        activeforeground="white",
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2",
    )


def make_form(root, title, width, height):
    form = tk.Toplevel(root)
    form.title(title)
    form.config(bg=PANEL_BG)
    form.grab_set()
    form.resizable(False, False)

    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2
    form.geometry(f"{width}x{height}+{x}+{y}")

    return form


def add_form_field(form, label_text, row, font_size, width=28):
    make_label(form, label_text, font_size).grid(
        row=row, column=0, padx=(20, 10), pady=8, sticky="e"
    )
    entry = make_entry(form, font_size, width=width)
    entry.grid(row=row, column=1, padx=(0, 20), pady=8, sticky="w")
    return entry


def run_main():
    pm = ma.PatientManager()
    dm = ma.DoctorManager()
    am = ma.AppointmentManager(pm, dm)

    window = tk.Tk()
    window.title("ClinicFlow")
    window.config(bg=BG)
    window.geometry("1200x1300")

    sf = scale_factor(window)
    menu_font_size = round(BASE_MENU_FONT_SIZE * sf)
    label_font_size = round(BASE_LABEL_FONT_SIZE * sf)
    input_font_size = round(BASE_INPUT_FONT_SIZE * sf)
    button_font_size = round(BASE_BUTTON_FONT_SIZE * sf)
    title_font_size = round(BASE_TITLE_FONT_SIZE * sf)

    menu_items = [
        "1.  Register A Patient",
        "2.  Add A Doctor",
        "3.  Book An Appointment",
        "4.  Cancel An Appointment",
        "5.  Complete An Appointment",
        "6.  View Patient Appointments",
        "7.  View Doctor Schedule",
        "8.  Search Patient By Name",
        "9.  Exit",
    ]

    container = tk.Frame(window, bg=BG)
    container.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        container,
        text="ClinicFlow",
        font=("Helvetica", title_font_size, "bold"),
        bg=BG,
        fg=ACCENT,
    ).pack(pady=(0, 10))

    tk.Label(
        container,
        text="What would you like to do?",
        font=("Helvetica", label_font_size + 2, "bold"),
        bg=BG,
        fg=FG,
    ).pack(pady=(0, 20))

    menu_frame = tk.Frame(container, bg=BG)
    menu_frame.pack(pady=(0, 30))

    for item in menu_items:
        tk.Label(
            menu_frame,
            text=item,
            font=("Helvetica", menu_font_size),
            bg=BG,
            fg=FG,
            anchor="w",
            justify="left",
        ).pack(fill="x", pady=4)

    input_label = tk.Label(
        container,
        text="Enter your choice number below:",
        font=("Helvetica", input_font_size),
        bg=BG,
        fg=MUTED_FG,
    )
    input_label.pack(pady=(10, 8))

    choice_input = tk.IntVar()
    input_entry = make_entry(container, input_font_size, width=10)
    input_entry.config(textvariable=choice_input)
    input_entry.pack(pady=(0, 20))
    input_entry.focus_set()

    status_label = tk.Label(
        container,
        text="",
        font=("Helvetica", label_font_size),
        bg=BG,
        fg="#ff8080",
        wraplength=600,
        justify="center",
    )

    def show_status(message, ok=False):
        status_label.config(text=message, fg="#6fdc8c" if ok else "#ff8080")
        status_label.pack(pady=(0, 10))

    def handle_choice():
        try:
            choice = int(input_entry.get())
        except ValueError:
            show_status("Error: Please enter a valid choice number.")
            return

        if choice == 1:
            form = make_form(window, "Register Patient", 420, 320)

            name_entry = add_form_field(form, "Name:", 0, input_font_size)
            age_entry = add_form_field(form, "Age:", 1, input_font_size)
            contact_entry = add_form_field(form, "Contact:", 2, input_font_size)
            patient_id_entry = add_form_field(form, "Patient ID:", 3, input_font_size)
            medical_history_entry = add_form_field(
                form, "Medical History\n(comma separated):", 4, input_font_size
            )

            def submit():
                try:
                    p_name = name_entry.get().strip()
                    p_age = int(age_entry.get().strip())
                    p_contact = int(contact_entry.get().strip())
                    p_id = patient_id_entry.get().strip()

                    medical_history = [
                        e.strip()
                        for e in medical_history_entry.get().split(",")
                        if e.strip()
                    ]

                    if not p_name or not p_id:
                        show_status("Error: Name and Patient ID cannot be empty!")
                        return

                    pm.add_patient(
                        name=p_name,
                        age=p_age,
                        contact=p_contact,
                        patient_id=p_id,
                        medical_history=medical_history,
                    )

                    show_status(f"Success: Registered patient {p_name}", ok=True)
                    form.destroy()

                except ValueError:
                    show_status(
                        "Error: Please enter valid numbers for Age and Contact."
                    )

            make_button(form, "Submit", submit, button_font_size).grid(
                row=5, column=0, columnspan=2, pady=16
            )

        elif choice == 2:
            d_form = make_form(window, "Register Doctor", 480, 400)

            d_name_entry = add_form_field(d_form, "Name:", 0, input_font_size)
            d_age_entry = add_form_field(d_form, "Age:", 1, input_font_size)
            d_contact_entry = add_form_field(d_form, "Contact:", 2, input_font_size)
            d_id_entry = add_form_field(d_form, "Doctor ID:", 3, input_font_size)
            d_specialization_entry = add_form_field(
                d_form, "Specialization:", 4, input_font_size
            )
            d_available_days_entry = add_form_field(
                d_form, "Available Days\n(comma separated):", 5, input_font_size
            )

            def submit_doctor():
                try:
                    name_val = d_name_entry.get().strip()
                    age_val = int(d_age_entry.get().strip())
                    contact_val = int(d_contact_entry.get().strip())
                    id_val = d_id_entry.get().strip()
                    spec_val = d_specialization_entry.get().strip()

                    days_list = [
                        day.strip()
                        for day in d_available_days_entry.get().split(",")
                        if day.strip()
                    ]

                    dm.add_doctor(
                        name=name_val,
                        age=age_val,
                        contact=contact_val,
                        doctor_id=id_val,
                        specialization=spec_val,
                        available_days=days_list,
                    )

                    show_status(f"Success: Registered Doctor {name_val}", ok=True)
                    d_form.destroy()

                except ValueError:
                    show_status("Error: Age and Contact must be valid integers.")

            make_button(d_form, "Submit", submit_doctor, button_font_size).grid(
                row=6, column=0, columnspan=2, pady=16
            )

        elif choice == 3:
            app_form = make_form(window, "Book Appointment", 420, 320)

            patient_id_for_app = add_form_field(
                app_form, "Patient ID:", 0, input_font_size
            )
            doctor_id_for_app = add_form_field(
                app_form, "Doctor ID:", 1, input_font_size
            )
            date_entry = add_form_field(
                app_form, "Date (YYYY-MM-DD):", 2, input_font_size
            )

            def submit_booking():
                am.book_appointment(
                    patient_id=patient_id_for_app.get().strip(),
                    doctor_id=doctor_id_for_app.get().strip(),
                    date=date_entry.get().strip(),
                )
                app_form.destroy()

            make_button(
                app_form, "Book Appointment", submit_booking, button_font_size
            ).grid(row=3, column=0, columnspan=2, pady=16)

        elif choice == 4:
            del_app_form = make_form(window, "Cancel Appointment", 400, 220)

            appointment_id_entry = add_form_field(
                del_app_form, "Appointment ID:", 0, input_font_size
            )

            def submit_cancel():
                am.cancel_appointment(appointment_id=appointment_id_entry.get().strip())
                del_app_form.destroy()

            make_button(
                del_app_form, "Cancel Appointment", submit_cancel, button_font_size
            ).grid(row=1, column=0, columnspan=2, pady=16)

        elif choice == 5:
            comp_app = make_form(window, "Complete Appointment", 400, 220)

            appointment_id_entry = add_form_field(
                comp_app, "Appointment ID:", 0, input_font_size
            )

            def submit_complete():
                am.complete_appointment(
                    appointment_id=appointment_id_entry.get().strip()
                )
                comp_app.destroy()

            make_button(
                comp_app, "Complete Appointment", submit_complete, button_font_size
            ).grid(row=1, column=0, columnspan=2, pady=16)

        elif choice == 6:
            patient_name_form = make_form(window, "View Patient Appointments", 420, 220)

            patient_id_entry = add_form_field(
                patient_name_form, "Patient ID:", 0, input_font_size
            )

            def submit_view_patient():
                for r in am.get_patient_appointments(
                    patient_id=patient_id_entry.get().strip()
                ):
                    print(r)
                patient_name_form.destroy()

            make_button(
                patient_name_form,
                "Fetch Appointments",
                submit_view_patient,
                button_font_size,
            ).grid(row=1, column=0, columnspan=2, pady=16)

        elif choice == 7:
            d_sch_form = make_form(window, "Doctor Schedule", 440, 260)

            doctor_id_entry = add_form_field(
                d_sch_form, "Doctor ID:", 0, input_font_size
            )
            date_needed_entry = add_form_field(
                d_sch_form, "Date (YYYY-MM-DD):", 1, input_font_size
            )

            def submit_view_schedule():
                for r in am.get_doctor_schedule(
                    doctor_id=doctor_id_entry.get().strip(),
                    date=date_needed_entry.get().strip(),
                ):
                    print(r)
                d_sch_form.destroy()

            make_button(
                d_sch_form, "Fetch Schedule", submit_view_schedule, button_font_size
            ).grid(row=2, column=0, columnspan=2, pady=16)

        elif choice == 8:
            p_name_form = make_form(window, "Search Patient", 420, 220)

            patient_name_entry = add_form_field(
                p_name_form, "Patient Name:", 0, input_font_size
            )

            def submit_search():
                for r in pm.find_patient(name=patient_name_entry.get().strip()):
                    print(r)
                p_name_form.destroy()

            make_button(
                p_name_form, "Search Database", submit_search, button_font_size
            ).grid(row=1, column=0, columnspan=2, pady=16)

        else:
            window.destroy()

    sub_btn = make_button(container, "Submit Choice", handle_choice, button_font_size)
    sub_btn.pack(pady=(0, 10))

    window.bind("<Return>", lambda e: handle_choice())

    window.mainloop()


if __name__ == "__main__":
    run_main()
