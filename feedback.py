import customtkinter as ctk
from tkinter import messagebox
from PUBLIC import *

def submit_feedback():
    feedback_con = feedback_text.get("1.0", ctk.END).strip()
    
    if not feedback_con or feedback_con == "Enter your feedback here...":
        messagebox.showwarning("Input Error", "Please enter your feedback!")
        return
    
    code = f"insert into feedback (stud_id,type,content) values('{Public.ID}','{selected_option.get()}','{feedback_con}')"
    
    inst_pub = Public()
    inst_pub.sql_connect(code=code,sel=2)
    
    feedback_text.delete("1.0", ctk.END)
    feedback_text.insert("1.0", "Enter your feedback here...")

def on_focus_in(event):
    if feedback_text.get("1.0", ctk.END).strip() == "Enter your feedback here...":
        feedback_text.delete("1.0", ctk.END)

def on_focus_out(event):
    if feedback_text.get("1.0", ctk.END).strip() == "":
        feedback_text.insert("1.0", "Enter your feedback here...")

def main_USER_FB(root):
    global feedback_text,selected_option
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ctk.CTkLabel(root, text="Feedback", font=("Arial", 25, "bold")).pack(pady=5)

    radio_frame = ctk.CTkFrame(root)
    radio_frame.pack(pady=10)

    selected_option = ctk.StringVar(value='S')

    radio1 = ctk.CTkRadioButton(master=radio_frame, text="Suggestion", variable=selected_option, value='S')
    radio1.pack(side="left", padx=10)

    radio2 = ctk.CTkRadioButton(master=radio_frame, text="Complaint", variable=selected_option, value="C")
    radio2.pack(side="left", padx=10)

    radio3 = ctk.CTkRadioButton(master=radio_frame, text="Review", variable=selected_option, value='R')
    radio3.pack(side="left", padx=10)

    feedback_text = ctk.CTkTextbox(root, width=500, height=300,font=("Helvetica", 15, "bold"))
    feedback_text.pack(pady=5, padx=3)
    feedback_text.insert("1.0", "Enter your feedback here...")

    feedback_text.bind("<FocusIn>", on_focus_in)
    feedback_text.bind("<FocusOut>", on_focus_out)

    submit_button = ctk.CTkButton(root, text="Submit", command=submit_feedback)
    submit_button.pack(pady=10)