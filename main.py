import json
import os
import tkinter as tk

# Imports the managers from the clinicflow folder you just downloaded and also since models is imported inside managers you don't need to worry about it
try:
    from clinicflow import managers as ma
except ModuleNotFoundError:
    print(
        "Error: couldn't find the 'clinicflow' package. Make sure the package clinicflow is a sibling to main.py."
    )
    raise SystemExit(1)

login_path = "data/login.json"
n_background = "#1e1e1e"  # Main background color (Dark theme because light mode is a crime to humanity)
n_foreground = "#e0e0e0"  # Standard text/font color
n_accent = "#4da3ff"  # Accent primary button color (Light Blue)


def scale_factor(window):
    window.update_idletasks()
    screen_h = window.winfo_screenheight()
    factor = screen_h / 1080
    return max(0.75, min(factor, 1.75))


def make_label(parent, text, size, bold=False, **kwargs):
    # bg and fg are always hardcoded to n_background / n_foreground. No light mode, no overrides.
    weight = "bold" if bold else "normal"
    bg = kwargs.pop("bg", n_background)
    fg = kwargs.pop("fg", n_foreground)

    return tk.Label(
        parent,
        text=text,
        font=("Helvetica", size, weight),
        bg=bg,
        fg=fg,
        **kwargs,
    )


def make_entry(parent, font_size, width=28):
    return tk.Entry(
        parent,
        bg=n_background,
        fg=n_foreground,
        insertbackground="white",
        font=("Helvetica", font_size),
        justify="left",
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
        bg=n_accent,
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
    form.config(bg=n_background)
    form.grab_set()  # Prevents interacting with main window while open
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


def blank_login():
    if not os.path.exists(login_path) or os.path.getsize(login_path) == 0:
        return True

    with open(login_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return True

    return not data.get("username") or not data.get("password")


def auth_screen():
    window = tk.Tk()
    window.title("ClinicFlow - Authentication")
    window.config(bg=n_background)
    window.geometry("1200x800")

    sf = scale_factor(window)
    label_font_size = round(15 * sf)
    input_font_size = round(18 * sf)
    button_font_size = round(16 * sf)
    title_font_size = round(30 * sf)

    container = tk.Frame(window, bg=n_background)
    container.place(relx=0.5, rely=0.5, anchor="center")

    def build_signup_form():
        for w in container.winfo_children():
            w.destroy()

        make_label(container, "Create Account", title_font_size, bold=True).pack(
            pady=(0, 20)
        )

        make_label(container, "Username:", label_font_size).pack()
        username_entry = make_entry(container, input_font_size, width=25)
        username_entry.pack(pady=(0, 10))

        make_label(container, "Password:", label_font_size).pack()
        password_entry = make_entry(container, input_font_size, width=25)
        password_entry.config(show="*")
        password_entry.pack(pady=(0, 10))

        status_label = make_label(container, "", label_font_size)

        def put_login_in_json():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            if not u or not p:
                status_label.config(text="Username and password can't be empty.")
                status_label.pack(pady=(5, 5))
                return

            os.makedirs(os.path.dirname(login_path), exist_ok=True)
            with open(login_path, "w") as f:
                json.dump({"username": u, "password": p}, f, indent=4)

            window.destroy()
            run_main()

        def no_sign():
            for w in container.winfo_children():
                w.destroy()

            make_label(
                container,
                "Are you sure? Your data will not be saved.",
                label_font_size,
                wraplength=500,
                justify="center",
            ).pack(pady=(0, 20))

            def proceed_without_login():
                window.destroy()
                run_main()

            make_button(
                container,
                "Yes, I am sure",
                proceed_without_login,
                button_font_size,
            ).pack(pady=8)
            make_button(
                container,
                "No thanks, take me back",
                build_signup_form,
                button_font_size,
            ).pack(pady=8)

        make_button(container, "Submit", put_login_in_json, button_font_size).pack(
            pady=10
        )
        make_button(
            container, "Continue without login", no_sign, button_font_size
        ).pack(pady=6)

    def build_login_form():
        with open(login_path, "r") as f:
            stored = json.load(f)

        make_label(
            parent=container, text="Login", size=title_font_size, bold=True
        ).pack(pady=(0, 20))

        make_label(parent=container, text="Username:", size=label_font_size).pack()
        username_entry = make_entry(container, input_font_size, width=25)
        username_entry.pack(pady=(0, 10))

        make_label(parent=container, text="Password:", size=label_font_size).pack()
        password_entry = make_entry(
            parent=container, font_size=input_font_size, width=25
        )
        password_entry.config(show="*")
        password_entry.pack(pady=(0, 10))

        status_label = make_label(parent=container, text="", size=label_font_size)

        def try_login():
            u = username_entry.get().strip()
            p = password_entry.get().strip()

            if u == stored.get("username") and p == stored.get("password"):
                window.destroy()
                run_main()
            elif u == stored.get("username") and p != stored.get("password"):
                status_label.config(text="Wrong password!")
                status_label.pack(pady=(5, 5))
            elif u != stored.get("username") and p == stored.get("password"):
                status_label.config(text="Wrong username!")
                status_label.pack(pady=(5, 5))
            else:
                status_label.config(text="Wrong username and password!")
                status_label.pack(pady=(5, 5))

        make_button(
            parent=container,
            text="Submit",
            command=try_login,
            font_size=button_font_size,
        ).pack(pady=10)

    if blank_login():
        build_signup_form()
    else:
        build_login_form()

    window.mainloop()


def run_main():
    pm = ma.PatientManager()
    dm = ma.DoctorManager()
    am = ma.AppointmentManager(pm, dm)

    window = tk.Tk()
    window.title("ClinicFlow - Dashboard")
    window.config(bg=n_background)
    window.geometry("1200x900")

    sf = scale_factor(window)
    menu_font_size = round(16 * sf)
    label_font_size = round(14 * sf)
    input_font_size = round(16 * sf)
    button_font_size = round(14 * sf)
    title_font_size = round(26 * sf)

    menu_items = [
        "1.  Register A Patient",
        "2.  Add A Doctor",
        "3.  Book An Appointment",
        "4.  Cancel An Appointment",
        "5.  Complete An Appointment",
        "6.  View Patient Appointments",
        "7.  View Doctor Schedule",
        "8.  Search Patient By Name",
        "9.  Delete Patient by Patient ID",
        "10. Delete Doctor by Doctor ID",
        "11. Reschedule Appointment",
        "12. View All Records",
        "13. Wipe Database",
        "14. Exit",
    ]

    container = tk.Frame(window, bg=n_background)
    container.place(relx=0.5, rely=0.5, anchor="center")

    make_label(
        container,
        "ClinicFlow",
        title_font_size,
        bold=True,
        fg=n_accent,
    ).pack(pady=(0, 10))

    make_label(
        container,
        "What would you like to do?",
        label_font_size + 2,
        bold=True,
    ).pack(pady=(0, 15))

    menu_frame = tk.Frame(container, bg=n_background)
    menu_frame.pack(pady=(0, 20))

    for item in menu_items:
        make_label(
            menu_frame,
            item,
            menu_font_size,
            anchor="w",
            justify="left",
        ).pack(fill="x", pady=2)

    make_label(
        container,
        "Enter your choice number below:",
        input_font_size,
    ).pack(pady=(10, 5))

    input_entry = tk.Entry(
        container,
        font=("Helvetica", input_font_size, "bold"),
        width=10,
        justify="center",
        bg=n_background,
        fg=n_foreground,
    )
    input_entry.pack(pady=(0, 15))
    input_entry.focus_set()

    status_label = make_label(
        container,
        "",
        label_font_size,
        fg="#ff8080",
        wraplength=600,
        justify="center",
    )

    def show_status(message: str, ok: bool = False):
        status_label.config(text=message, fg="#6fdc8c" if ok else "#ff8080")
        status_label.pack(pady=(0, 10))

    def handle_choice():
        try:
            choice = int(input_entry.get().strip())
        except ValueError:
            show_status("Error: Please enter a valid choice number.")
            return

        # Calls the pm.add_patient() func to register the patient
        match choice:
            case 1:
                form = make_form(window, "Register Patient", 450, 360)

                name_entry = add_form_field(form, "Name:", 0, input_font_size)
                age_entry = add_form_field(form, "Age:", 1, input_font_size)
                contact_entry = add_form_field(form, "Contact:", 2, input_font_size)
                patient_id_entry = add_form_field(
                    form, "Patient ID:", 3, input_font_size
                )
                medical_history_entry = add_form_field(
                    form,
                    "Medical History\n(comma separated):",
                    4,
                    input_font_size,
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

            # Calls the dm.add_doctor() func to register the doctor also d here is short for doctor
            case 2:
                d_form = make_form(window, "Register Doctor", 480, 420)

                d_name_entry = add_form_field(d_form, "Name:", 0, input_font_size)
                d_age_entry = add_form_field(d_form, "Age:", 1, input_font_size)
                d_contact_entry = add_form_field(d_form, "Contact:", 2, input_font_size)
                d_id_entry = add_form_field(d_form, "Doctor ID:", 3, input_font_size)
                d_specialization_entry = add_form_field(
                    d_form, "Specialization:", 4, input_font_size
                )
                d_available_days_entry = add_form_field(
                    d_form,
                    "Available Days\n(comma separated):",
                    5,
                    input_font_size,
                )

                def submit_doctor():
                    try:
                        name_val = d_name_entry.get().strip()  # val is shart for value
                        age_val = int(d_age_entry.get().strip())
                        contact_val = int(d_contact_entry.get().strip())
                        id_val = d_id_entry.get().strip()
                        spec_val = d_specialization_entry.get().strip()

                        days_list = [
                            day.strip()
                            for day in d_available_days_entry.get().split(",")
                            if day.strip()
                        ]  # Runs a list comprehension with all whitespaces(at the start and end) of each day stripped(by .strip())
                        # for the day in the entry(it's split by commas which is why the input says to write it comma-seperated)

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

            # Calls am.book_appointment() simple enough
            case 3:
                app_form = make_form(window, "Book Appointment", 450, 280)

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
                    show_status("Appointment booked successfully!", ok=True)
                    app_form.destroy()

                make_button(
                    app_form,
                    "Book Appointment",
                    submit_booking,
                    button_font_size,
                ).grid(row=3, column=0, columnspan=2, pady=16)

            # Cancels the appointment. Once again, am.cancel_appointment()
            case 4:
                del_app_form = make_form(window, "Cancel Appointment", 400, 200)

                appointment_id_entry = add_form_field(
                    del_app_form, "Appointment ID:", 0, input_font_size
                )

                def submit_cancel():
                    am.cancel_appointment(
                        appointment_id=appointment_id_entry.get().strip()
                    )
                    show_status("Appointment cancelled.", ok=True)
                    del_app_form.destroy()

                make_button(
                    del_app_form,
                    "Cancel Appointment",
                    submit_cancel,
                    button_font_size,
                ).grid(row=1, column=0, columnspan=2, pady=16)

            # Calls am.complete_appointment() to show that the appointment has been completed
            case 5:
                comp_app = make_form(window, "Complete Appointment", 400, 200)

                appointment_id_entry = add_form_field(
                    comp_app, "Appointment ID:", 0, input_font_size
                )

                def submit_complete():
                    am.complete_appointment(
                        appointment_id=appointment_id_entry.get().strip()
                    )
                    show_status("Appointment marked completed.", ok=True)
                    comp_app.destroy()

                make_button(
                    comp_app,
                    "Complete Appointment",
                    submit_complete,
                    button_font_size,
                ).grid(row=1, column=0, columnspan=2, pady=16)

            # Used for viewing all the appointments of the specific patient using am.get_patient_appointments()
            case 6:
                patient_name_form = make_form(
                    window, "View Patient Appointments", 420, 200
                )

                patient_id_entry = add_form_field(
                    patient_name_form, "Patient ID:", 0, input_font_size
                )

                def submit_view_patient():
                    results = am.get_patient_appointments(
                        patient_id=patient_id_entry.get().strip()
                    )
                    for r in results:
                        print(r)
                    show_status(f"Fetched {len(results)} appointment records.", ok=True)
                    patient_name_form.destroy()

                make_button(
                    patient_name_form,
                    "Fetch Appointments",
                    submit_view_patient,
                    button_font_size,
                ).grid(row=1, column=0, columnspan=2, pady=16)

            # Gets the schedule of the doctor by calling am.get_doctor_schedule()
            case 7:
                d_schedule_form = make_form(window, "Doctor Schedule", 440, 240)

                doctor_id_entry = add_form_field(
                    d_schedule_form, "Doctor ID:", 0, input_font_size
                )
                date_needed_entry = add_form_field(
                    d_schedule_form, "Date (YYYY-MM-DD):", 1, input_font_size
                )

                def submit_view_schedule():
                    results = am.get_doctor_schedule(
                        doctor_id=doctor_id_entry.get().strip(),
                        date=date_needed_entry.get().strip(),
                    )
                    for r in results:
                        print(r)
                    show_status(f"Fetched schedule with {len(results)} items.", ok=True)
                    d_schedule_form.destroy()

                make_button(
                    d_schedule_form,
                    "Fetch Schedule",
                    submit_view_schedule,
                    button_font_size,
                ).grid(row=2, column=0, columnspan=2, pady=16)

            # Searchs for the patient by name
            case 8:
                p_name_form = make_form(window, "Search Patient", 420, 200)

                patient_name_entry = add_form_field(
                    p_name_form, "Patient Name:", 0, input_font_size
                )

                def submit_search():
                    results = pm.find_patient(name=patient_name_entry.get().strip())
                    for r in results:
                        print(r)
                    show_status(f"Found {len(results)} matching records.", ok=True)
                    p_name_form.destroy()

                make_button(
                    p_name_form,
                    "Search Database",
                    submit_search,
                    button_font_size,
                ).grid(row=1, column=0, columnspan=2, pady=16)

            # Deletes the patient by calling pm.remove_patient()
            case 9:
                patient_removal_form = make_form(window, "Delete Patient", 420, 200)

                make_label(
                    patient_removal_form, "Enter Patient ID:", label_font_size
                ).pack(pady=(20, 5))
                patient_id_entry = make_entry(
                    patient_removal_form, input_font_size, width=20
                )
                patient_id_entry.pack(pady=(0, 15))

                def submit_remove_patient():
                    p_id = patient_id_entry.get().strip()
                    if pm.remove_patient(p_id):
                        print(f"Patient {p_id} successfully removed.")
                        show_status(f"Patient {p_id} successfully removed.", ok=True)
                    else:
                        print(f"Patient with ID {p_id} not found.")
                        show_status(f"Patient with ID {p_id} not found.")
                    patient_removal_form.destroy()

                make_button(
                    patient_removal_form,
                    "Delete Patient",
                    submit_remove_patient,
                    button_font_size,
                ).pack(pady=10)

            # Deletes the doctor by calling dm.remove_doctor() also d is short for doctor
            case 10:
                d_removal_form = make_form(window, "Delete Doctor", 420, 200)

                make_label(d_removal_form, "Enter Doctor ID:", label_font_size).pack(
                    pady=(20, 5)
                )
                d_id_entry = make_entry(d_removal_form, input_font_size, width=20)
                d_id_entry.pack(pady=(0, 15))

                def submit_remove_doctor():
                    d_id = d_id_entry.get().strip()
                    if dm.remove_doctor(d_id):
                        print(f"Doctor with ID {d_id} successfully removed.")
                        show_status(
                            f"Doctor with ID {d_id} successfully removed.",
                            ok=True,
                        )
                    else:
                        print(f"Doctor with ID {d_id} not found.")
                        show_status(f"Doctor with ID {d_id} not found.")
                    d_removal_form.destroy()

                make_button(
                    d_removal_form,
                    "Delete Doctor",
                    submit_remove_doctor,
                    button_font_size,
                ).pack(pady=10)

            case 11:
                resched_form = make_form(window, "Reschedule Appointment", 440, 240)

                appointment_id_entry = add_form_field(
                    resched_form, "Appointment ID:", 0, input_font_size
                )
                new_date_entry = add_form_field(
                    resched_form, "New Date (YYYY-MM-DD):", 1, input_font_size
                )

                def submit_reschedule():
                    a_id = appointment_id_entry.get().strip()
                    new_date = new_date_entry.get().strip()
                    error = am.reschedule_appointment(a_id, new_date)
                    if error is None:
                        show_status(
                            f"Appointment {a_id} rescheduled to {new_date}.", ok=True
                        )
                    else:
                        show_status(error)
                    resched_form.destroy()

                make_button(
                    resched_form,
                    "Reschedule",
                    submit_reschedule,
                    button_font_size,
                ).grid(row=2, column=0, columnspan=2, pady=16)

            case 12:
                view_all_form = make_form(window, "View All Records", 420, 220)

                make_label(
                    view_all_form,
                    "Choose what to list (results print to console).",
                    label_font_size,
                    justify="center",
                ).pack(pady=(20, 15))

                btn_frame = tk.Frame(view_all_form, bg=n_background)
                btn_frame.pack(pady=10)

                def do_view_patients():
                    results = [p.get_summary() for p in pm.patient_dict.values()]
                    for r in results:
                        print(r)
                    show_status(
                        f"Listed {len(results)} patients (see console).", ok=True
                    )
                    view_all_form.destroy()

                def do_view_doctors():
                    results = [d.get_summary() for d in dm.doctor_dict.values()]
                    for r in results:
                        print(r)
                    show_status(
                        f"Listed {len(results)} doctors (see console).", ok=True
                    )
                    view_all_form.destroy()

                def do_view_appointments():
                    results = [a.get_summary() for a in am.appointments.values()]
                    for r in results:
                        print(r)
                    show_status(
                        f"Listed {len(results)} appointments (see console).", ok=True
                    )
                    view_all_form.destroy()

                make_button(
                    btn_frame, "Patients", do_view_patients, button_font_size
                ).pack(side="left", padx=5)
                make_button(
                    btn_frame, "Doctors", do_view_doctors, button_font_size
                ).pack(side="left", padx=5)
                make_button(
                    btn_frame, "Appointments", do_view_appointments, button_font_size
                ).pack(side="left", padx=5)

            # The func to wipe databases
            case 13:
                confirm_form = make_form(window, "Wipe Options", 520, 260)

                make_label(
                    confirm_form,
                    "Select which database entity you want to wipe.\n"
                    "Warning: You cannot undo this action. All data will be permanently gone!",
                    label_font_size,
                    justify="center",
                ).pack(pady=(20, 15))

                btn_frame = tk.Frame(confirm_form, bg=n_background)
                btn_frame.pack(pady=10)

                def do_pm_wipe():
                    pm.wipe()
                    show_status("Patient database wiped.", ok=True)
                    confirm_form.destroy()

                def do_dm_wipe():
                    dm.wipe()
                    show_status("Doctor database wiped.", ok=True)
                    confirm_form.destroy()

                def do_am_wipe():
                    am.wipe()
                    show_status("Appointments database wiped.", ok=True)
                    confirm_form.destroy()

                # Does not use button func because the bg and fg used here is different
                tk.Button(
                    btn_frame,
                    text="Wipe Patients",
                    command=do_pm_wipe,
                    bg="#c0392b",
                    fg="white",
                    relief="flat",
                    padx=8,
                    pady=6,
                    cursor="hand2",
                ).pack(side="left", padx=5)

                tk.Button(
                    btn_frame,
                    text="Wipe Doctors",
                    command=do_dm_wipe,
                    bg="#d35400",
                    fg="white",
                    relief="flat",
                    padx=8,
                    pady=6,
                    cursor="hand2",
                ).pack(side="left", padx=5)

                tk.Button(
                    btn_frame,
                    text="Wipe Appointments",
                    command=do_am_wipe,
                    bg="#8e44ad",
                    fg="white",
                    relief="flat",
                    padx=8,
                    pady=6,
                    cursor="hand2",
                ).pack(side="left", padx=5)

                tk.Button(
                    btn_frame,
                    text="Cancel",
                    command=confirm_form.destroy,
                    bg="#444444",
                    fg="white",
                    relief="flat",
                    padx=8,
                    pady=6,
                    cursor="hand2",
                ).pack(side="left", padx=5)

            case 14:
                window.destroy()

            case _:
                show_status("Error: Please enter a number from 1 to 14.")

    sub_btn = make_button(container, "Submit Choice", handle_choice, button_font_size)
    sub_btn.pack(pady=(0, 10))

    window.bind("<Return>", lambda e: handle_choice())
    window.mainloop()


if __name__ == "__main__":
    auth_screen()
