from customtkinter import *
from mysql.connector import *
from Gpass import *

def Sub_Clicked():
    content = text.get("1.0", "end").strip()
    Form_check = GPASS(entry1.get(), entry2.get(), entry3.get(), content, entry5.get())
    Form_check.check_form_validity(entry1, entry2, entry3, text, entry5)
    Form_check.Save_Data(entry1, entry2, entry3, text, entry5)

def Gate_con(parent_frame):
    global text, entry1, entry2, entry3, entry5
    
    # Clear the right frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_rowconfigure(0, weight=1)
    parent_frame.grid_rowconfigure(9, weight=1)

    title = CTkLabel(master=parent_frame, text="Leave Form", text_color="black", font=("Arial", 24))
    title.grid(row=0, column=0, padx=0.1, pady=0.1)

    entry1 = CTkEntry(master=parent_frame, placeholder_text="Enter Name", placeholder_text_color="green", border_color="grey")
    entry1.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    entry2 = CTkEntry(master=parent_frame, placeholder_text="Date of leaving (dd-mm-yyyy)", placeholder_text_color="green")
    entry2.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    entry3 = CTkEntry(master=parent_frame, placeholder_text="Date of entering (dd-mm-yyyy)", placeholder_text_color="green")
    entry3.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    title = CTkLabel(master=parent_frame, text="Reason For Leaving", text_color="black", font=("Arial", 15))
    title.grid(row=4, column=0, padx=0.1, pady=0.1)

    text = CTkTextbox(master=parent_frame, scrollbar_button_color="blue", corner_radius=20, height=100)
    text.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    entry5 = CTkEntry(master=parent_frame, placeholder_text="Student ID", placeholder_text_color="green")
    entry5.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

    # Submit button
    btn = CTkButton(master=parent_frame, text="SUBMIT", corner_radius=32, fg_color="blue", hover_color="red", command=Sub_Clicked)
    btn.grid(row=7, column=0, padx=20, pady=20)

    entry1.insert(0, 'Amal')
    entry2.insert(0, '01/11/2024')
    entry3.insert(0, '29/11/2024')
    entry5.insert(0, '12354')