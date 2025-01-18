import customtkinter as ctk
from PUBLIC import *
from tkinter import messagebox

def main_notification(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)
    frame.grid_columnconfigure(2, weight=2)
    frame.grid_columnconfigure(3, weight=1)

    header_label = ctk.CTkLabel(frame, text="Notifications", font=("Arial", 16, "bold"))
    header_label.grid(row=0, column=0, columnspan=4, padx=5, pady=10, sticky="ew")

    checkbox_vars = []
    stud_ids = []
    selected_msg = []

    public_inst = Public()
    public_inst.sql_connect("SELECT COUNT(*) FROM feedback", 1)
    row_c = public_inst.resultArr[0][0]
    
    public_inst.sql_connect("SELECT stud_id, type, status, fb_no FROM feedback", 1)

    view_buttons = {}

    for row in range(row_c):
        stud_id = public_inst.resultArr[row][0]
        
        cb_var = ctk.IntVar()
        checkbox = ctk.CTkCheckBox(frame, variable=cb_var, text="", command=lambda r=row: on_checkbox_change(r))
        checkbox.grid(row=row + 1, column=0, padx=(30, 5), pady=5, sticky="nsew")
        checkbox_vars.append(cb_var)
        
        sno = public_inst.resultArr[row][3]
        status = public_inst.resultArr[row][2]

        for col in range(2):
            if col == 0:
                label_text = stud_id
            else:
                feedback_type = public_inst.resultArr[row][col]
                label_text = {
                    'S': "SUGGESTION",
                    'C': "COMPLAINT",
                    'R': "REVIEW"
                }.get(feedback_type, "UNKNOWN")

            label = ctk.CTkLabel(frame, text=label_text)
            label.grid(row=row + 1, column=col + 1, padx=5, pady=5, sticky="nsew")

        stud_ids.append(stud_id)
        
        button_color = "green" if status == 1 else "orange" if status == 2 else "red"
        
        view_button = ctk.CTkButton(
            frame,
            text="View",
            fg_color=button_color,
            text_color="white",
            command=lambda sid=stud_id, fb_no=sno: open_top_level(sid, fb_no)
        )
        view_button.grid(row=row + 1, column=3, padx=(5, 10), pady=5, sticky="nsew")
        
        view_buttons[sno] = view_button

    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(pady=10)

    select_all_button = ctk.CTkButton(bottom_frame, text="Select All", command=lambda: toggle_select_all(), width=100)
    select_all_button.grid(row=0, column=0, padx=10)

    clear_all_button = ctk.CTkButton(bottom_frame, text="Clear All", command=lambda: clear_all(checkbox_vars), width=100)
    clear_all_button.grid(row=0, column=1, padx=10)

    def toggle_select_all():
        if all(cb_var.get() == 1 for cb_var in checkbox_vars):
            clear_all(checkbox_vars)
        else:
            select_all(checkbox_vars)

    def select_all(checkbox_vars):
        for cb_var in checkbox_vars:
            cb_var.set(1)
        select_all_button.configure(text="Unselect All")

    def clear_all(checkbox_vars):
        # Identify selected feedbacks
        selected_feedbacks = [public_inst.resultArr[i][3] for i, cb_var in enumerate(checkbox_vars) if cb_var.get() == 1]
        
        # Delete selected feedbacks from the database
        if selected_feedbacks:
            for fb_no in selected_feedbacks:
                if fb_no != 2:
                    public_inst.sql_connect(f"DELETE FROM feedback WHERE fb_no = '{fb_no}'", 0)
                else:
                    messagebox.showwarning("", "Trying to delete saved notification!")
                    
        for cb_var in checkbox_vars:
            cb_var.set(0)
            
        select_all_button.configure(text="Select All")


    def on_checkbox_change(row):
        if all(cb_var.get() == 1 for cb_var in checkbox_vars):
            select_all_button.configure(text="Unselect All")
        elif all(cb_var.get() == 0 for cb_var in checkbox_vars):
            select_all_button.configure(text="Select All")
        else:
            select_all_button.configure(text="Unselect All")

        print_selected(row)

    def print_selected(row):
        if checkbox_vars[row].get() == 1:
            stud_id = stud_ids[row]
            print(f"Row {row + 1} selected with stud_id: {stud_id}")

    def open_top_level(stud_id, fb_no):
        public_inst.sql_connect(f"UPDATE feedback SET status = 1 WHERE fb_no = '{fb_no}'", 0)
        
        if fb_no in view_buttons:
            view_buttons[fb_no].configure(fg_color="green")

        try:
            public_inst.sql_connect(
                f"SELECT A.f_name, A.l_name, A.email, A.contact, A.room_id, A.roll_no, A.class, A.section, B.content, B.type "
                f"FROM student A, Feedback B "
                f"WHERE B.stud_id='{stud_id}' AND fb_no={fb_no} AND A.stud_id=B.stud_id", 1
            )
            
            details = public_inst.resultArr[0]

            top_level_window = ctk.CTkToplevel(root)
            top_level_window.title(f"Details for {stud_id}")
            top_level_window.transient(root)
            top_level_window.grab_set()
            root.attributes("-disabled", True)

            def on_close():
                root.attributes("-disabled", False)
                top_level_window.destroy()

            top_level_window.protocol("WM_DELETE_WINDOW", on_close)

            frame_x = root.winfo_x()
            frame_y = root.winfo_y()
            frame_width = root.winfo_width()
            frame_height = root.winfo_height()
            
            top_level_window.geometry(f"{frame_width}x{frame_height}+{frame_x}+{frame_y}")

            content_frame = ctk.CTkFrame(top_level_window)
            content_frame.pack(pady=20, padx=20, fill="both", expand=True)

            labels_text = [
                ("Name:", f"{details[0]} {details[1]}"),
                ("Email:", details[2]),
                ("Contact No:", details[3]),
                ("Room No:", details[4]),
                ("Roll No:", details[5]),
                ("Class:", details[6]),
                ("Section:", details[7]),
                ("Type:", details[9]),
                ("Message:", details[8])
            ]

            for i, (label_text, value_text) in enumerate(labels_text):
                label = ctk.CTkLabel(content_frame, text=label_text, font=("Arial", 12))
                label.grid(row=i, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="ew")

                border_frame = ctk.CTkFrame(content_frame, border_width=1, corner_radius=5)
                border_frame.grid(row=i, column=2, columnspan=2, padx=10, pady=(5, 0), sticky="ew")

                value = ctk.CTkLabel(border_frame, text=value_text, font=("Arial", 12))
                value.pack(padx=5, pady=5, anchor="center")

            def on_save():
                public_inst.sql_connect(
                    f"UPDATE feedback SET status = 2 WHERE fb_no = '{fb_no}'", 0)
                view_buttons[fb_no].configure(fg_color="orange")
                on_close()

            save_button = ctk.CTkButton(top_level_window, text="Save", command=on_save)
            save_button.pack(pady=(10, 5))

            close_button = ctk.CTkButton(top_level_window, text="Close", command=on_close)
            close_button.pack(pady=5)
            
        except Exception as e:
            print(f"Error: {e}")