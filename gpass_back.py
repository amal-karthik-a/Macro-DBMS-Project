import customtkinter as ctk
from PUBLIC import *
import datetime
from tkinter import messagebox

def agree_fun(g_id):
  Public_inst.sql_connect(f"update check_out set status = 'Agreed' where g_id = {g_id}",1)
  close_top_level(details_window)
  
def decline_fun(g_id):
  Public_inst.sql_connect(f"update check_out set status = 'Declined' where g_id = '{g_id}'",1)
  close_top_level(details_window)
  
def show_student_details(stud_id, root,g_id):
    global details_window
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

    # Create a frame for the buttons
    button_frame = ctk.CTkFrame(details_window)
    button_frame.pack(pady=20, side="bottom")

    # Close, Agree, and Decline buttons in the same row and centered
    close_button = ctk.CTkButton(button_frame, text="Close", command=lambda: close_top_level(details_window))
    close_button.grid(row=0, column=0, padx=10)

    agree_button = ctk.CTkButton(button_frame, text="Agree", command=lambda: agree_fun(g_id))
    agree_button.grid(row=0, column=1, padx=10)

    decline_button = ctk.CTkButton(button_frame, text="Decline", command=lambda: decline_fun(g_id))
    decline_button.grid(row=0, column=2, padx=10)

    # Configure grid to center-align buttons
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

    details_window.protocol("WM_DELETE_WINDOW", lambda: close_top_level(details_window))

def close_top_level(details_window):
    details_window.grab_release()  # Re-enable the root window
    details_window.destroy()

def main_gpas(root):
    global Public_inst
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Main frame for centering content
    main_frame = ctk.CTkFrame(root, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Frame for headers and data, aligned to the center
    frame = ctk.CTkFrame(main_frame, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Center header labels in the specified order
    header_labels = ["Profile", "Id", "Out Date", "In Date", "Purpose"]
    for i, header in enumerate(header_labels):
        label = ctk.CTkLabel(frame, text=header, font=("Arial", 14, "bold"), width=80)
        label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

    # Configure grid columns to center-align contents
    for i in range(len(header_labels)):
        frame.columnconfigure(i, weight=1)

    # Connect to database and fetch data
    Public_inst = Public()
    Public_inst.sql_connect("SELECT COUNT(*) FROM check_out", 1)
    rows = Public_inst.resultArr[0][0]

    Public_inst.sql_connect("SELECT * FROM check_out", 1)
    data = Public_inst.resultArr

    for row in range(1, rows + 1):
        stud_id = data[row - 1][0]
        check_out_date = data[row - 1][1] if data[row - 1][1] is not None else "N/A"
        check_in_date = data[row - 1][2] if data[row - 1][2] is not None else "N/A"
        status = data[row - 1][3] if data[row - 1][3] is not None else "N/A"
        purpose = data[row - 1][4] if data[row - 1][4] is not None else "N/A"
        g_id = data[row - 1][5] if data[row - 1][5] is not None else "N/A"

        button_color = "green" if status != "N/A" else "red"

        # View button with color based on status
        view_button = ctk.CTkButton(
            frame, text="View", fg_color=button_color, text_color="white", width=60,
            command=lambda stud_id=stud_id: show_student_details(stud_id, root,g_id)
        )
        view_button.grid(row=row, column=0, padx=5, pady=5)

        # Display data in labels centered in each cell
        ctk.CTkLabel(frame, text=stud_id, width=80, anchor="center").grid(row=row, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame, text=check_out_date, width=80, anchor="center").grid(row=row, column=2, padx=5, pady=5)
        ctk.CTkLabel(frame, text=check_in_date, width=80, anchor="center").grid(row=row, column=3, padx=5, pady=5)
        ctk.CTkLabel(frame, text=purpose, width=80, anchor="center").grid(row=row, column=4, padx=5, pady=5)

    # Bottom frame for navigation buttons centered
    bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    bottom_frame.pack(pady=10)
