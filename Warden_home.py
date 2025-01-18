import customtkinter as ctk
from PIL import Image, ImageTk
from PUBLIC import *
from LeavE_ForM import *
from datetime import *
from notification import *
from due_fee import *
from gpass_back import *

def load_data(id_load):
    global Public_inst
    Public_inst = Public()
    Public_inst.sql_connect(f"select * from student where stud_id='{id_load}'",1)

# Declare entries as a global variable to access it within save_data
entries = {}

import mysql.connector

def new_stud():
    global entries
    new_inst = Public()
    entries = {}  # Initialize the dictionary to store entry fields
    # Clear previous entries if any
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Define the fields based on your table columns
    fields = [
        "First name", "Last name", "email", "contact", "address", 
        "passout_yr", "room_id", "PM_name", "PF_Name", "P_contact", 
        "remark", "dob", "gender", "class", "section", "roll_no", "adm_no"
    ]

    # Create labels and entries for each field
    for index, field in enumerate(fields):
        label = ctk.CTkLabel(right_frame, text=field.capitalize(), font=("Arial", 14),text_color="white")
        label.grid(row=index, column=0, sticky="w", padx=10, pady=5)

        entry = ctk.CTkEntry(right_frame, width=250, font=("Arial", 12),fg_color="#2F2C2C",text_color="white")
        entry.grid(row=index, column=1, padx=10, pady=5)
        
        entries[field] = entry  # Store the entry widget in the dictionary

    def save():
        data = {field: entry.get() for field, entry in entries.items()}
        new_inst.sql_connect(f"select * from student where adm_no = '{data['adm_no']}'",1)
        
        if len(new_inst.resultArr) == 0:
            try:
                insert_query = f"""INSERT INTO student (stud_id, f_name, l_name, email, contact, address, passout_yr,room_id, PM_name, PF_Name, P_contact, remark, dob,gender, class, section, roll_no, adm_no) VALUES ('S{data['adm_no']}','{data['First name']}', '{data['Last name']}', '{data['email']}', {data['contact']}, '{data['address']}', {data['passout_yr']}, {data['room_id']}, '{data['PM_name']}', '{data['PF_Name']}', '{data['P_contact']}', '{data['remark']}', '{data['dob']}', '{data['gender']}', '{data['class']}', '{data['section']}', {data['roll_no']}, {data['adm_no']})"""
                
                """today = date.today()
                future_date = today + timedelta(days=10)
                
                new_inst.sql_connect(f"insert into fee values('S{data['adm_no']}',27000,4000,NULL,NULL,'{future_date}')",0) """
                
                new_inst.sql_connect(insert_query,0)
                
                new_inst.sql_connect(f"select passwd from login where stud_id = 'S{data['adm_no']}'",1)
                
                msg = f'''Your details have been added to the hotel and the registration process is completed and you can now access the student portal and the login credentials are :\nUser Id : S{data['adm_no']}\n Password : {new_inst.resultArr[0][0]}'''
                new_inst.sent_Mail("From Hostel Warden",msg,{data['email']})

                messagebox.showinfo("New Student","Login Credentials are send to respective student mail !")
            except Exception as e:
                messagebox.showwarning("Data",f"Invalid data found ! \nError : {e}")
        else:
            messagebox.showwarning("New Student","Invalid Admission Number Entered !")

    save_button = ctk.CTkButton(right_frame, text="Save", width=100, font=("Arial", 14, "bold"), command=save)
    save_button.grid(row=len(fields), column=1, pady=(20, 10))


def main_notification_run():
    for widget in right_frame.winfo_children():
        widget.destroy()
    main_notification(right_frame)

def load_data(id_load):
    global Public_inst
    Public_inst = Public()
    Public_inst.sql_connect(f"select * from student where stud_id='{id_load}'", 1)

def main_notification_run():
    for widget in right_frame.winfo_children():
        widget.destroy()
    main_notification(right_frame)

def main_fee_due():
    for widget in right_frame.winfo_children():
        widget.destroy()
    main_fee(right_frame)
    
def main_gpas_run():
    for widget in right_frame.winfo_children():
        widget.destroy()
    main_gpas(right_frame)

def center_window(window, width=1350, height=950):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    
def logout_fun(root):
    Public.Member = ""
    Public.ID = ""
    root.destroy()
    
def show_content(content):
    for widget in right_frame.winfo_children():
        widget.destroy()
    content_label = ctk.CTkLabel(right_frame, text=content, font=("Arial", 20))
    content_label.pack(pady=20)

def logout():
    Public.Member = ""
    Public.ID = ""
    app_stud.destroy()

def home_warden_dash():
    global app_stud, bottom_frame, right_frame, upper_frame
    app_stud = ctk.CTk()
    app_stud.geometry("1350x950")
    app_stud.title("Student Dashboard")
    app_stud.configure(fg_color="#1E1E1E")

    center_window(app_stud)
    left_frame = ctk.CTkFrame(app_stud, width=300, fg_color="transparent")  # Transparent background
    left_frame.pack(side="left", fill="y", padx=20, pady=20)

    # Upper frame for profile details
    upper_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    upper_frame.pack(fill="x", padx=10, pady=(10, 5))

    # Date label in the upper frame
    date_label = ctk.CTkLabel(upper_frame, text=f"Date : {datetime.date.today()}", font=("Arial", 12))
    date_label.pack(anchor="w", padx=5, pady=(10, 5))  # Left aligned

    # Enlarged Student label
    student_label = ctk.CTkLabel(upper_frame, text="WARDEN", font=("Monoton", 24, "bold"))
    student_label.pack(pady=(10, 5))

    bottom_frame = ctk.CTkFrame(left_frame, fg_color="#2F2C2C")
    bottom_frame.pack(fill="x", expand=True, padx=10, pady=(5, 10))

    # Define the buttons and their respective actions
    buttons = {
        "Add new Student":lambda:new_stud(),
        "View Request": lambda: main_gpas_run(),
        "Fee Status": lambda: main_fee_due(),
        "Notifications": lambda: main_notification_run()
    }

    # Loop through the buttons and create them
    for text, command in buttons.items():
        btn = ctk.CTkButton(bottom_frame, text=text, command=command, width=260, height=40, fg_color="#393939", hover_color="#938989", font=("Poppins", 15, "bold"))
        btn.pack(pady=10, padx=20)

    logout_button = ctk.CTkButton(bottom_frame, text="Log Out", command=logout, fg_color="red", width=260, height=40, font=("Poppins", 13, 'bold'))
    logout_button.pack(pady=(30, 20), padx=20)

    right_frame = ctk.CTkFrame(app_stud, corner_radius=10, width=900, height=850, border_width=2, border_color="#826A6A", fg_color="#2F2C2C")
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    app_stud.mainloop()