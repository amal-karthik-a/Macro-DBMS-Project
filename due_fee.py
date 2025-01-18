import customtkinter as ctk
from PUBLIC import *
import datetime
from tkinter import messagebox

def Alert_Email():
    Public_inst.sql_connect(f"select A.stud_id,A.email,A.f_name,A.l_name,A.class,A.section,B.due_date,B.mess,B.rent from student A,fee B where B.stud_id = A.stud_id and paid_date is NULL",1)
    
    for i in Public_inst.resultArr:
        msg = f'''From Warden Hostel FISAT ,

Student id : {i[0]}
Student Name : {i[2]}  {i[3]}
Class : {i[4]} {i[5]}
        
The student hasn't paid the hostel fee amount of {int(i[7])+int(i[8])} /- before Last date {str(i[6])} .
        
If the fee is not paid by today {datetime.date.today()}, a fine of 500 /- per week will be charged if there is no valid reason.
        
If already paid, please ignore this email.
'''
        Public_inst.sent_Mail("Late fee", msg, str(i[1]))
        messagebox.showinfo("Alert","Alert send Successfully !")

def show_student_details(stud_id,root):
    
    details_window = ctk.CTkToplevel(root)
    details_window.title("Student Details")

    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    details_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
    
    details_window.transient(root)
    
    details_window.grab_set()   
    
    Public_inst.sql_connect(f"SELECT stud_id,f_name,l_name,class,section,contact FROM student WHERE stud_id = '{stud_id}'", 1)
    student_data = Public_inst.resultArr[0]

    # Display student details in the top-level window
    ctk.CTkLabel(details_window, text=f"Student ID: {student_data[0]}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(details_window, text=f"Name: {student_data[1]} {student_data[2]}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(details_window, text=f"Class: {student_data[3]}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(details_window, text=f"Section: {student_data[4]}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(details_window, text=f"Contact: {student_data[5]}", font=("Arial", 14)).pack(pady=5)

    close_button = ctk.CTkButton(details_window, text="Close", command=lambda: close_top_level(details_window))
    close_button.pack(pady=20, side="bottom")
    
    details_window.protocol("WM_DELETE_WINDOW", lambda: close_top_level(details_window))

def close_top_level(details_window):
    details_window.grab_release()  # Re-enable the root window
    details_window.destroy()

def main_fee(root):
    global Public_inst
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Set header labels in the specified order
    header_labels = ["Profile", "Id", "Due Fee", "Due Date", "Paid Date"]
    for i, header in enumerate(header_labels):
        label = ctk.CTkLabel(frame, text=header, font=("Arial", 14, "bold"), width=80)
        label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

    # Connect to database and fetch data
    Public_inst = Public()
    Public_inst.sql_connect("SELECT COUNT(*) FROM fee", 1)
    rows = Public_inst.resultArr[0][0]

    Public_inst.sql_connect("SELECT * FROM fee", 1)
    data = Public_inst.resultArr

    for row in range(1, rows + 1):
        # Extract data for each column
        stud_id = data[row - 1][0]
        rent = data[row - 1][1] if data[row - 1][1] is not None else 0
        mess = data[row - 1][2] if data[row - 1][2] is not None else 0
        due_fee = rent + mess  # Calculate due fee
        due_date = data[row - 1][5] if data[row - 1][5] is not None else "N/A"
        paid_date = data[row - 1][3] if data[row - 1][3] is not None else None

        # Determine button color based on payment status
        button_color = "green" if paid_date else "red"

        # Display View button with conditional color
        view_button = ctk.CTkButton(
            frame, text="View", fg_color=button_color, text_color="white", width=60,
            command=lambda stud_id=stud_id: show_student_details(stud_id,root)
        )
        view_button.grid(row=row, column=0, padx=5, pady=5)

        # Display data in labels in the specified order
        ctk.CTkLabel(frame, text=stud_id, width=80).grid(row=row, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame, text=due_fee, width=80).grid(row=row, column=2, padx=5, pady=5)
        ctk.CTkLabel(frame, text=due_date, width=80).grid(row=row, column=3, padx=5, pady=5)
        ctk.CTkLabel(frame, text=paid_date if paid_date else "Unpaid", width=80).grid(row=row, column=4, padx=5, pady=5)

    # Bottom frame with navigation buttons
    bottom_frame = ctk.CTkFrame(root, fg_color="grey")
    bottom_frame.pack(pady=10)
    
    alert_button = ctk.CTkButton(bottom_frame, text="Alert", width=100, command=Alert_Email)
    alert_button.grid(row=0, column=1, padx=10)