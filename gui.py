
import tkinter as tk
from tkinter import messagebox
from booking_rules import check_booking_rules



from database import (
    register_user,
    get_all_campuses,
    login_user,
    get_resources_by_campus,
    add_booking,
    get_user_bookings,
    cancel_booking,
    get_bookings_by_campus,
    get_all_resources_by_campus,
    add_resource,
    set_resource_status,
    get_all_bookings,
    get_most_used_resources,
    get_average_booking_duration,

)


def open_window():
    window = tk.Tk()
    window.title("Smart Campus Resource Booking System")
    window.geometry("700x450")
    window.configure(bg="#F5F2EA")

    heading = tk.Label(
        window,
        text="SMART CAMPUS",
        font=("Arial", 25, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=(55, 5))

    subtitle = tk.Label(
        window,
        text="RESOURCE BOOKING SYSTEM",
        font=("Arial", 12, "bold"),
        bg="#F5F2EA",
        fg="#168C85"
    )
    subtitle.pack(pady=5)

    message = tk.Label(
        window,
        text="Welcome!\nBook resources. Manage spaces. Connect campuses.",
        font=("Arial", 11),
        bg="#F5F2EA",
        fg="#454545",
        justify="center"
    )
    message.pack(pady=25)

    login_button = tk.Button(
        window,
        text="LOGIN",
        font=("Arial", 11, "bold"),
        bg="#168C85",
        fg="white",
        width=20,
        pady=8,
        cursor="hand2",
        command=open_login_screen
    )
    login_button.pack(pady=8)

    register_button = tk.Button(
        window,
        text="CREATE ACCOUNT",
        font=("Arial", 11, "bold"),
        bg="#173B3F",
        fg="white",
        width=20,
        pady=8,
        cursor="hand2",
        command=open_register_screen
    )
    register_button.pack(pady=5)

    footer = tk.Label(
        window,
        text="A smarter way to manage campus resources",
        font=("Arial", 9, "italic"),
        bg="#F5F2EA",
        fg="#666666"
    )
    footer.pack(side="bottom", pady=18)

    window.mainloop()


def open_login_screen():
    login_window = tk.Toplevel()
    login_window.title("Login - Smart Campus Resource Booking System")
    login_window.geometry("450x350")
    login_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        login_window,
        text="Welcome Back",
        font=("Arial", 20, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=(30, 20))

    username_label = tk.Label(
        login_window,
        text="Username",
        font=("Arial", 11),
        bg="#F5F2EA",
        fg="#454545"
    )
    username_label.pack()

    username_entry = tk.Entry(
        login_window,
        font=("Arial", 12),
        width=28
    )
    username_entry.pack(pady=5)

    password_label = tk.Label(
        login_window,
        text="Password",
        font=("Arial", 11),
        bg="#F5F2EA",
        fg="#454545"
    )
    password_label.pack(pady=(10, 0))

    password_entry = tk.Entry(
        login_window,
        font=("Arial", 12),
        width=28,
        show="*"
    )
    password_entry.pack(pady=5)

    login_message = tk.Label(
        login_window,
        text="Enter your account details to continue.",
        font=("Arial", 9),
        bg="#F5F2EA",
        fg="#666666"
    )
    login_message.pack(pady=10)

    def check_login():
        username = username_entry.get().strip()
        password = password_entry.get()

        if username == "" or password == "":
            login_message.config(
                text="Please enter your username and password.",
                fg="red"
            )
            return


        user = login_user(username, password)

        if user is not None:

            try:
                full_name = user["full_name"]
                role = user["role"]
            except (TypeError, IndexError):
                full_name = user[1]
                role = user[4]


            login_message.config(
                text="Login successful! Welcome, " + full_name
                + ". Your role is: " + role,
                fg="#168C85"
            )

            login_button.config(state="disabled")

            if role == "Lecturer":
                try:
                    campus_id = user["campus_id"]
                except (TypeError, IndexError):
                    campus_id = user[5]

                open_lecturer_dashboard(
                    full_name,
                    campus_id,
                    user[0]
                )

            elif role == "Campus Administrator":
                try:
                    campus_id = user["campus_id"]
                except (TypeError, IndexError):
                    campus_id = user[5]

                open_admin_dashboard(
                    full_name,
                    campus_id,
                    user[0]
                )

            elif role == "System Operator":
                open_system_operator_dashboard(full_name)




        else:
            login_message.config(
                text="Incorrect username or password.",
                fg="red"
            )


    login_button = tk.Button(
        login_window,
        text="LOGIN",
        font=("Arial", 11, "bold"),
        bg="#168C85",
        fg="white",
        width=20,
        pady=8,
        cursor="hand2",
        command=check_login
    )
    login_button.pack(pady=5)



def open_register_screen():
    register_window = tk.Toplevel()
    register_window.title(
        "Create Account - Smart Campus Resource Booking System"
    )
    register_window.geometry("450x480")
    register_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        register_window,
        text="Create Your Account",
        font=("Arial", 19, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=(20, 15))

    name_label = tk.Label(
        register_window,
        text="Full Name",
        bg="#F5F2EA",
        fg="#454545"
    )
    name_label.pack()

    name_entry = tk.Entry(
        register_window,
        font=("Arial", 11),
        width=30
    )
    name_entry.pack(pady=4)

    username_label = tk.Label(
        register_window,
        text="Choose a Username",
        bg="#F5F2EA",
        fg="#454545"
    )
    username_label.pack()

    username_entry = tk.Entry(
        register_window,
        font=("Arial", 11),
        width=30
    )
    username_entry.pack(pady=4)

    password_label = tk.Label(
        register_window,
        text="Choose a Password",
        bg="#F5F2EA",
        fg="#454545"
    )
    password_label.pack()

    password_entry = tk.Entry(
        register_window,
        font=("Arial", 11),
        width=30,
        show="*"
    )
    password_entry.pack(pady=4)

    campus_label = tk.Label(
        register_window,
        text="Select Your Campus",
        font=("Arial", 10, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    campus_label.pack(pady=(10, 3))

    campus_list = get_all_campuses()
    campus_names = [campus[1] for campus in campus_list]

    campus_dropdown = tk.StringVar(register_window)

    if campus_names:
        campus_dropdown.set(campus_names[0])
    else:
        campus_dropdown.set("No campuses available")

    campus_menu = tk.OptionMenu(
        register_window,
        campus_dropdown,
        *campus_names
    )

    role_dropdown = tk.StringVar(register_window)
    role_dropdown.set("Lecturer")

    def update_campus_options(selected_role):
        if selected_role == "System Operator":
            campus_dropdown.set("Not required")
            campus_menu.config(state="disabled")

        else:
            campus_menu.config(state="normal")

            if campus_names:
                campus_dropdown.set(campus_names[0])
            else:
                campus_dropdown.set("No campuses available")


    role_menu = tk.OptionMenu(
        register_window,
        role_dropdown,
        "Lecturer",
        command=update_campus_options
    )

    role_menu.config(
        font=("Arial", 10),
        bg="white",
        fg="#173B3F",
        width=25
    )

    role_menu.pack(pady=5)

    campus_menu.config(
        font=("Arial", 10),
        bg="white",
        fg="#173B3F",
        width=25
    )
    campus_menu.pack(pady=5)

    register_message = tk.Label(
        register_window,
        text="",
        font=("Arial", 10),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    register_message.pack(pady=5)


    def create_account():
        full_name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get()
        selected_campus = campus_dropdown.get()
        role = role_dropdown.get()

        if full_name == "" or username == "" or password == "":
            register_message.config(
                text="Please fill in all fields.",
                fg="red"
            )
            return

        if not campus_names:
            register_message.config(
                text="No campuses are available. Please try again later.",
                fg="red"
            )
            return

        campus_id = None

        if role != "System Operator":
            for campus in campus_list:
                if campus[1] == selected_campus:
                    campus_id = campus[0]
                    break

            if campus_id is None:
                register_message.config(
                    text="Please select a valid campus.",
                    fg="red"
                )
                return

        success = register_user(
            full_name,
            username,
            password,
            role,
            campus_id
        )

        if success:
            register_message.config(
                text="Account created successfully!",
                fg="#168C85"
            )
        else:
            register_message.config(
                text="Username already exists. Try another.",
                fg="red"
            )

    create_button = tk.Button(
        register_window,
        text="CREATE ACCOUNT",
        font=("Arial", 11, "bold"),
        bg="#168C85",
        fg="white",
        width=20,
        pady=8,
        cursor="hand2",
        command=create_account
    )
    create_button.pack(pady=5)

def open_lecturer_dashboard(full_name, campus_id, user_id):
    dashboard = tk.Toplevel()
    dashboard.title("Lecturer Dashboard")
    dashboard.geometry("700x450")
    dashboard.configure(bg="#F5F2EA")

    heading = tk.Label(
        dashboard,
        text="LECTURER DASHBOARD",
        font=("Arial", 22, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    welcome = tk.Label(
        dashboard,
        text="Welcome, " + full_name + "!",
        font=("Arial", 14),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    welcome.pack(pady=10)

    information = tk.Label(
        dashboard,
        text="Manage your campus resource bookings here.",
        font=("Arial", 11),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    information.pack(pady=10)


    view_resources_button = tk.Button(
        dashboard,
        text="View Available Resources",
        font=("Arial", 11),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: view_available_resources(campus_id),
        pady=6
    )
    view_resources_button.pack(pady=6)

    make_booking_button = tk.Button(
        dashboard,
        text="Make a Booking",
        font=("Arial", 11),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: open_booking_window(full_name, campus_id, user_id),
        pady=6
    )
    make_booking_button.pack(pady=6)

    booking_history_button = tk.Button(
        dashboard,
        text="View Booking History",
        font=("Arial", 11),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: view_booking_history(user_id),
        pady=6
    )
    booking_history_button.pack(pady=6)


    cancel_booking_button = tk.Button(
        dashboard,
        text="Cancel a Booking",
        font=("Arial", 11),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: open_cancel_booking_window(user_id),
        pady=6
    )
    cancel_booking_button.pack(pady=6)





def view_all_system_resources():


    from database import get_all_resources

    resources = get_all_resources()

    resources_window = tk.Toplevel()
    resources_window.title("All Campus Resources")
    resources_window.geometry("750x500")
    resources_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        resources_window,
        text="ALL CAMPUS RESOURCES",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    if not resources:
        message = tk.Label(
            resources_window,
            text="No resources have been added yet.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)

    else:
        for resource in resources:
            resource_text = (
                "Resource ID: " + str(resource[0])
                + " | Code: " + str(resource[1])
                + " | Name: " + str(resource[2])
                + " | Type: " + str(resource[3])
                + " | Campus Name: " + str(resource[4])
                + " | Status: "
                + ("Active" if resource[5] == 1 else "Inactive")
            )

            resource_label = tk.Label(
                resources_window,
                text=resource_text,
                font=("Arial", 10),
                bg="#F5F2EA",
                fg="#173B3F",
                wraplength=700,
                justify="left"
            )
            resource_label.pack(anchor="w", padx=15, pady=5)



def view_campus_comparison_reports():

    campuses = get_all_campuses()
    bookings = get_all_bookings()
    most_used_resources = get_most_used_resources()
    average_duration = get_average_booking_duration()

    reports_window = tk.Toplevel()
    reports_window.title("Campus Comparison Reports")
    reports_window.geometry("700x600")
    reports_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        reports_window,
        text="CAMPUS COMPARISON REPORT",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    overall_total = len(bookings)

    overall_label = tk.Label(
        reports_window,
        text="Total bookings across all campuses: " + str(overall_total),
        font=("Arial", 12, "bold"),
        bg="#F5F2EA",
        fg="#168C85"
    )
    overall_label.pack(pady=8)


    for campus in campuses:
        campus_name = campus[1]
        total_bookings = 0

        for booking in bookings:
            if booking[3] == campus_name:
                total_bookings += 1

        report_text = (
            campus_name
            + " | Total bookings: "
            + str(total_bookings)
        )

        report_label = tk.Label(
            reports_window,
            text=report_text,
            font=("Arial", 12),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        report_label.pack(pady=5)


    average_label = tk.Label(
        reports_window,
        text="Average active booking duration: "
        + str(average_duration)
        + " hours",
        font=("Arial", 12, "bold"),
        bg="#F5F2EA",
        fg="#168C85"
    )
    average_label.pack(pady=12)


    resource_heading = tk.Label(
        reports_window,
        text="MOST-USED RESOURCES",
        font=("Arial", 14, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    resource_heading.pack(pady=10)

    if not most_used_resources:
        resource_label = tk.Label(
            reports_window,
            text="No active bookings to report yet.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        resource_label.pack(pady=5)
    else:
        for resource in most_used_resources:
            resource_text = (
                resource[0]
                + " | "
                + resource[1]
                + " | Active bookings: "
                + str(resource[2])
            )

            resource_label = tk.Label(
                reports_window,
                text=resource_text,
                font=("Arial", 11),
                bg="#F5F2EA",
                fg="#173B3F"
            )
            resource_label.pack(pady=3)


def view_all_system_bookings():


    bookings = get_all_bookings()

    bookings_window = tk.Toplevel()
    bookings_window.title("All Campus Bookings")
    bookings_window.geometry("900x550")
    bookings_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        bookings_window,
        text="ALL CAMPUS BOOKINGS",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    if not bookings:
        message = tk.Label(
            bookings_window,
            text="No bookings have been recorded yet.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)

    else:
        for booking in bookings:
            booking_text = (
                "Booking ID: " + str(booking[0])
                + " | Lecturer: " + str(booking[1])
                + " | Resource: " + str(booking[2])
                + " | Campus: " + str(booking[3])
                + " | Date: " + str(booking[4])
                + " | Time: " + str(booking[5])
                + " | Duration: " + str(booking[6]) + " hour(s)"
                + " | Status: " + str(booking[7])
            )

            booking_label = tk.Label(
                bookings_window,
                text=booking_text,
                font=("Arial", 9),
                bg="#F5F2EA",
                fg="#173B3F",
                wraplength=850,
                justify="left"
            )
            booking_label.pack(anchor="w", padx=15, pady=5)

def open_system_operator_dashboard(full_name):


    dashboard = tk.Toplevel()
    dashboard.title("System Operator Dashboard")
    dashboard.geometry("700x500")
    dashboard.configure(bg="#F5F2EA")

    heading = tk.Label(
        dashboard,
        text="SYSTEM OPERATOR",
        font=("Arial", 20, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    welcome = tk.Label(
        dashboard,
        text="Welcome, " + full_name,
        font=("Arial", 12),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    welcome.pack(pady=5)

    bookings_button = tk.Button(
        dashboard,
        text="View All Campus Bookings",
        font=("Arial", 12),
        bg="#168C85",
        fg="white",
        width=30,
        command=view_all_system_bookings
    )
    bookings_button.pack(pady=10)

    resources_button = tk.Button(
        dashboard,
        text="View All Campus Resources",
        font=("Arial", 12),
        bg="#168C85",
        fg="white",
        width=30,
        command=view_all_system_resources
    )
    resources_button.pack(pady=10)

    reports_button = tk.Button(
        dashboard,
        text="View Campus Comparison Reports",
        font=("Arial", 12),
        bg="#168C85",
        fg="white",
        width=30,
        command=view_campus_comparison_reports
    )
    reports_button.pack(pady=10)


def open_admin_dashboard(full_name, campus_id, user_id):


    dashboard = tk.Toplevel()
    dashboard.title("Campus Administrator Dashboard")
    dashboard.geometry("700x500")
    dashboard.configure(bg="#F5F2EA")

    heading = tk.Label(
        dashboard,
        text="CAMPUS ADMINISTRATOR",
        font=("Arial", 20, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    welcome = tk.Label(
        dashboard,
        text="Welcome, " + full_name,
        font=("Arial", 12),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    welcome.pack(pady=5)

    campus_label = tk.Label(
        dashboard,
        text="Your assigned Campus ID: " + str(campus_id),
        font=("Arial", 11),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    campus_label.pack(pady=5)


    manage_button = tk.Button(
        dashboard,
        text="Manage Campus Resources",
        font=("Arial", 12),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: manage_campus_resources(campus_id)
    )
    manage_button.pack(pady=10)


    bookings_button = tk.Button(
        dashboard,
        text="View Campus Bookings",
        font=("Arial", 12),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: view_campus_bookings(campus_id)
    )
    bookings_button.pack(pady=10)


    availability_button = tk.Button(
        dashboard,
        text="View Resource Availability",
        font=("Arial", 12),
        bg="#168C85",
        fg="white",
        width=30,
        command=lambda: view_resource_availability(campus_id)
    )
    availability_button.pack(pady=10)





def change_resource_status(resource_id, campus_id, active, refresh_function=None):

    success = set_resource_status(
        resource_id,
        campus_id,
        active
    )

    if success:
        messagebox.showinfo(
            "Resource Updated",
            "Resource status updated successfully."
        )

        if refresh_function is not None:
            refresh_function()
    else:
        messagebox.showerror(
            "Update Failed",
            "The resource status could not be changed."
        )




def view_resource_availability(campus_id):


    resources = get_all_resources_by_campus(campus_id)

    availability_window = tk.Toplevel()
    availability_window.title("Resource Availability")
    availability_window.geometry("650x450")
    availability_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        availability_window,
        text="RESOURCE AVAILABILITY",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=20)

    if not resources:
        message = tk.Label(
            availability_window,
            text="No resources have been added to this campus yet.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)

    else:
        for resource in resources:
            resource_code = resource[1]
            resource_name = resource[2]
            resource_type = resource[3]

            if resource[4] == 1:
                status = "Active"
            else:
                status = "Inactive"

            resource_text = (
                resource_code + " - " + resource_name
                + " (" + resource_type + ")"
                + " | Status: " + status
            )

            resource_label = tk.Label(
                availability_window,
                text=resource_text,
                font=("Arial", 10),
                bg="#F5F2EA",
                fg="#173B3F"
            )
            resource_label.pack(pady=5)

def manage_campus_resources(campus_id):


    resources = get_all_resources_by_campus(campus_id)

    resources_window = tk.Toplevel()
    resources_window.title("Manage Campus Resources")
    resources_window.geometry("750x500")
    resources_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        resources_window,
        text="MANAGE CAMPUS RESOURCES",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=15)


    resource_list_frame = tk.Frame(
        resources_window,
        bg="#F5F2EA"
    )
    resource_list_frame.pack(fill="both", expand=True, padx=10, pady=5)



    def refresh_resource_list():
        for widget in resource_list_frame.winfo_children():
            widget.destroy()

        resources = get_all_resources_by_campus(campus_id)

        if not resources:
            message = tk.Label(
                resource_list_frame,
                text="No resources have been added to this campus yet.",
                font=("Arial", 11),
                bg="#F5F2EA",
                fg="#173B3F"
            )
            message.pack(pady=10)
            return

        for resource in resources:
            status = "Active" if resource[4] == 1 else "Inactive"

            resource_text = (
                "Code: " + str(resource[1])
                + " | Name: " + str(resource[2])
                + " | Type: " + str(resource[3])
                + " | Status: " + status
            )

            resource_label = tk.Label(
                resource_list_frame,
                text=resource_text,
                font=("Arial", 10),
                bg="#F5F2EA",
                fg="#173B3F",
                wraplength=700,
                justify="left"
            )
            resource_label.pack(anchor="w", padx=15, pady=5)

            new_status = 0 if resource[4] == 1 else 1

            button_text = (
                "Deactivate Resource"
                if resource[4] == 1
                else "Activate Resource"
            )

            status_button = tk.Button(
                resource_list_frame,
                text=button_text,
                font=("Arial", 9),
                bg="#168C85",
                fg="white",
                command=lambda r_id=resource[0], s=new_status:
                change_resource_status(r_id, campus_id, s, refresh_resource_list)
            )
            status_button.pack(pady=3)

    refresh_resource_list()


    form_heading = tk.Label(
        resources_window,
        text="ADD A NEW RESOURCE",
        font=("Arial", 13, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    form_heading.pack(pady=10)

    code_label = tk.Label(
        resources_window,
        text="Resource Code:",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    code_label.pack()

    code_entry = tk.Entry(resources_window, width=30)
    code_entry.pack(pady=3)

    name_label = tk.Label(
        resources_window,
        text="Resource Name:",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    name_label.pack()

    name_entry = tk.Entry(resources_window, width=30)
    name_entry.pack(pady=3)

    type_label = tk.Label(
        resources_window,
        text="Resource Type:",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    type_label.pack()

    type_entry = tk.Entry(resources_window, width=30)
    type_entry.pack(pady=3)


    def save_resource():
        resource_code = code_entry.get().strip()
        resource_name = name_entry.get().strip()
        resource_type = type_entry.get().strip()

        if not resource_code or not resource_name or not resource_type:
            result_label.config(
                text="Please complete all three fields.",
                fg="red"
            )
            return

        success = add_resource(
            resource_code,
            resource_name,
            resource_type,
            campus_id
        )

        if success:
            result_label.config(
                text="Resource added successfully!",
                fg="#168C85"
            )
            code_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            type_entry.delete(0, tk.END)
            refresh_resource_list()
        else:
            result_label.config(
                text="Could not add resource. Check its code.",
                fg="red"
            )

    save_button = tk.Button(
        resources_window,
        text="Save Resource",
        font=("Arial", 11, "bold"),
        bg="#168C85",
        fg="white",
        width=20,
        command=save_resource
    )
    save_button.pack(pady=10)

    result_label = tk.Label(
        resources_window,
        text="",
        font=("Arial", 10),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    result_label.pack(pady=5)



def view_campus_bookings(campus_id):


    bookings = get_bookings_by_campus(campus_id)

    bookings_window = tk.Toplevel()
    bookings_window.title("Campus Bookings")
    bookings_window.geometry("850x500")
    bookings_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        bookings_window,
        text="CAMPUS BOOKINGS",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=15)

    if not bookings:
        message = tk.Label(
            bookings_window,
            text="There are no bookings for this campus yet.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)
        return

    for booking in bookings:
        booking_text = (
            "Booking ID: " + str(booking[0])
            + " | Lecturer: " + str(booking[1])
            + " | Resource: " + str(booking[2])
            + " | Campus: " + str(booking[3])
            + " | Date: " + str(booking[4])
            + " | Time: " + str(booking[5])
            + " | Duration: " + str(booking[6]) + " hour(s)"
            + " | Status: " + str(booking[7])
        )

        booking_label = tk.Label(
            bookings_window,
            text=booking_text,
            font=("Arial", 9),
            bg="#F5F2EA",
            fg="#173B3F",
            wraplength=800,
            justify="left"
        )
        booking_label.pack(anchor="w", padx=15, pady=5)


def open_cancel_booking_window(user_id):

    bookings = get_user_bookings(user_id)

    cancel_window = tk.Toplevel()
    cancel_window.title("Cancel a Booking")
    cancel_window.geometry("750x400")
    cancel_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        cancel_window,
        text="CANCEL A BOOKING",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=15)

    active_bookings = []

    for booking in bookings:
        if booking[7] == "Active":
            active_bookings.append(booking)

    if not active_bookings:
        message = tk.Label(
            cancel_window,
            text="You have no active bookings to cancel.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)
        return

    booking_choices = []

    for booking in active_bookings:
        choice = (
            "ID: " + str(booking[0])
            + " | Resource: " + str(booking[8])
            + " | Campus: " + str(booking[9])
            + " | Date: " + str(booking[4])
            + " | Time: " + str(booking[5])
            + " | Duration: " + str(booking[6]) + " hour(s)"
        )
        booking_choices.append(choice)

    selected_booking = tk.StringVar(cancel_window)
    selected_booking.set(booking_choices[0])

    booking_menu = tk.OptionMenu(
        cancel_window,
        selected_booking,
        *booking_choices
    )
    booking_menu.config(width=80)
    booking_menu.pack(pady=10)

    cancel_message = tk.Label(
        cancel_window,
        text="",
        font=("Arial", 10),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    cancel_message.pack(pady=5)

    def confirm_cancellation():
        selected_text = selected_booking.get()
        booking_id = int(
            selected_text.split(" | ")[0].replace("ID: ", "")
        )

        success = cancel_booking(booking_id, user_id)

        if success:
            cancel_message.config(
                text="Booking cancelled successfully!",
                fg="#168C85"
            )
            cancel_window.after(1000, cancel_window.destroy)
        else:
            cancel_message.config(
                text="Cancellation failed. It may have already started.",
                fg="red"
            )

    cancel_button = tk.Button(
        cancel_window,
        text="CONFIRM CANCELLATION",
        font=("Arial", 11, "bold"),
        bg="#168C85",
        fg="white",
        command=confirm_cancellation,
        pady=6
    )
    cancel_button.pack(pady=10)



def view_booking_history(user_id):

    bookings = get_user_bookings(user_id)

    history_window = tk.Toplevel()
    history_window.title("My Booking History")
    history_window.geometry("750x450")
    history_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        history_window,
        text="MY BOOKING HISTORY",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=15)

    if not bookings:
        message = tk.Label(
            history_window,
            text="You have not made any bookings yet.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)
        return

    for booking in bookings:
        booking_text = (
            "Booking ID: " + str(booking[0])
            + " | Resource: " + str(booking[8])
            + " | Campus: " + str(booking[9])
            + " | Date: " + str(booking[4])
            + " | Start time: " + str(booking[5])
            + " | Duration: " + str(booking[6]) + " hour(s)"
            + " | Status: " + str(booking[7])
        )

        booking_label = tk.Label(
            history_window,
            text=booking_text,
            font=("Arial", 10),
            bg="#F5F2EA",
            fg="#173B3F",
            wraplength=700,
            justify="left"
        )
        booking_label.pack(anchor="w", padx=15, pady=5)


def view_available_resources(campus_id):
    resources = get_resources_by_campus(campus_id)

    resource_window = tk.Toplevel()
    resource_window.title("Available Campus Resources")
    resource_window.geometry("600x400")
    resource_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        resource_window,
        text="AVAILABLE RESOURCES",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=15)

    if not resources:
        message = tk.Label(
            resource_window,
            text="No resources are currently available.",
            font=("Arial", 11),
            bg="#F5F2EA",
            fg="#173B3F"
        )
        message.pack(pady=10)

    else:
        for resource in resources:
            resource_text = (
                "Code: " + str(resource[1])
                + " | Name: " + str(resource[2])
                + " | Type: " + str(resource[3])
            )

            resource_label = tk.Label(
                resource_window,
                text=resource_text,
                font=("Arial", 10),
                bg="#F5F2EA",
                fg="#173B3F"
            )
            resource_label.pack(pady=5)

def open_booking_window(full_name, campus_id, user_id):
    booking_window = tk.Toplevel()
    booking_window.title("Make a Booking")
    booking_window.geometry("550x450")
    booking_window.configure(bg="#F5F2EA")

    heading = tk.Label(
        booking_window,
        text="MAKE A BOOKING",
        font=("Arial", 18, "bold"),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    heading.pack(pady=15)

    welcome = tk.Label(
        booking_window,
        text="Lecturer: " + full_name,
        font=("Arial", 11),
        bg="#F5F2EA",
        fg="#173B3F"
    )
    welcome.pack(pady=5)

    resource_label = tk.Label(
        booking_window,
        text="Select a resource:",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    resource_label.pack(pady=5)

    resources = get_resources_by_campus(campus_id)
    resource_choices = []

    for resource in resources:
        resource_choices.append(
            str(resource[0]) + " - " + resource[2]
        )

    resource_choice = tk.StringVar(booking_window)

    if resource_choices:
        resource_choice.set(resource_choices[0])
    else:
        resource_choice.set("No resources available")

    resource_menu = tk.OptionMenu(
        booking_window,
        resource_choice,
        *resource_choices
    )
    resource_menu.pack(pady=5)

    date_label = tk.Label(
        booking_window,
        text="Booking date (YYYY-MM-DD):",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    date_label.pack(pady=5)

    date_entry = tk.Entry(
        booking_window,
        font=("Arial", 11),
        width=25
    )
    date_entry.pack(pady=5)

    time_label = tk.Label(
        booking_window,
        text="Start time (HH:MM, 24-hour format):",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    time_label.pack(pady=5)

    time_entry = tk.Entry(
        booking_window,
        font=("Arial", 11),
        width=25
    )
    time_entry.pack(pady=5)

    duration_label = tk.Label(
        booking_window,
        text="Duration in hours:",
        bg="#F5F2EA",
        fg="#173B3F"
    )
    duration_label.pack(pady=5)

    duration_entry = tk.Entry(
        booking_window,
        font=("Arial", 11),
        width=25
    )
    duration_entry.pack(pady=5)

    booking_message = tk.Label(
        booking_window,
        text="Enter your booking details above.",
        font=("Arial", 10),
        bg="#F5F2EA",
        fg="#173B3F",
        wraplength=450
    )
    booking_message.pack(pady=10)

    def submit_booking():
        if not resource_choices:
            booking_message.config(
                text="No resources are available to book.",
                fg="red"
            )
            return

        selected_resource = resource_choice.get()
        resource_id = int(selected_resource.split(" - ")[0])

        booking_date = date_entry.get().strip()
        from datetime import datetime, date

        try:
            selected_date = datetime.strptime(
                booking_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            booking_message.config(
                text="Please enter a valid date in YYYY-MM-DD format.",
                fg="red"
            )
            return

        if selected_date < date.today():
            booking_message.config(
                text="You cannot book a resource for a past date.",
                fg="red"
            )
            return
        start_time = time_entry.get().strip()
        duration_text = duration_entry.get().strip()

        if booking_date == "" or start_time == "" or duration_text == "":
            booking_message.config(
                text="Please fill in all booking details.",
                fg="red"
            )
            return

        try:
            duration = int(duration_text)
        except ValueError:
            booking_message.config(
                text="Duration must be a whole number of hours.",
                fg="red"
            )
            return

        campuses = get_all_campuses()
        campus_name = ""

        for campus in campuses:
            if campus[0] == campus_id:
                campus_name = campus[1]
                break

        rules_ok, rules_message = check_booking_rules(
            campus_name,
            start_time,
            duration
        )

        if not rules_ok:
            booking_message.config(
                text=rules_message,
                fg="red"
            )
            return

        success = add_booking(
            user_id,
            resource_id,
            campus_id,
            booking_date,
            start_time,
            duration
        )

        if success:
            booking_message.config(
                text="Booking created successfully!",
                fg="#168C85"
            )
        else:
            booking_message.config(
                text="Booking could not be created. Check the date, time, duration, campus rules, or resource availability.",
                fg="red"
            )

    book_button = tk.Button(
        booking_window,
        text="BOOK RESOURCE",
        font=("Arial", 11, "bold"),
        bg="#168C85",
        fg="white",
        width=25,
        pady=6,
        command=submit_booking
    )
    book_button.pack(pady=10)


if __name__ == "__main__":
    open_window()
