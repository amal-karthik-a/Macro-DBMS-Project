from customtkinter import *
from PUBLIC import *
from tkinter import messagebox
import time

count_atmpt = 0
    
def done():
    global entry_username, entry_password, root, count_atmpt
    inst_pub = Public()
    if len(entry_username.get()) == 0:
        label_info.configure(text="User name is Mandatory !")
        entry_username.configure(border_color="red")
    elif len(entry_password.get()) == 0:
        label_info.configure(text="Password is Mandatory !")
        entry_password.configure(border_color="red")
    else:
        entry_password.configure(border_color="grey")
        entry_username.configure(border_color="grey")
            
        inst_pub.sql_connect(f"select passwd from login where stud_id = '{entry_username.get()}'", 1)
        count_atmpt += 1
        try:
            if inst_pub.resultArr[0][0] == entry_password.get():
                Member = entry_username.get().strip()
                if Member[0] == 'S':
                    Public.Member = 'S'
                elif Member[0] == 'W':
                    Public.Member = 'W'
                Public.ID = entry_username.get().strip()
                del inst_pub
                root.after_cancel("all")
                root.quit()
                root.destroy()
                
            else:
                label_info.configure(text=f"Login Denied [ Attempt : {count_atmpt} ] !")
        except Exception:
            label_info.configure(text=f"Login Denied [ Attempt : {count_atmpt} ] !")
        if count_atmpt == 5:
            entry_password.configure(state="disabled")
            entry_username.configure(state="disabled")
            label_info.configure(text="Login Disabled !")
            messagebox.showerror("Login", "Login Denied for 5th Attempt !")
            time.sleep(0.3)
            Public.on_closing(root)

def main_login():
    global root, login_frame, entry_password, entry_username, button_login, label_info
    root = CTk()
    root.title("Login Page")
    root.geometry("450x500")
    root.maxsize(450, 500)
    root.minsize(450, 500)
    root.protocol("WM_DELETE_WINDOW", lambda:Public.on_closing(root)) 

    login_frame = CTkFrame(root)
    login_frame.pack(pady=80, padx=30, fill="both", expand=True)

    label_login = CTkLabel(login_frame, text="LOGIN", font=("Arial", 24, "bold", "underline"))
    label_login.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="ew")  

    label_username = CTkLabel(login_frame, text="UserID:", font=("Arial", 12, "bold"))
    label_username.grid(row=1, column=0, padx=0, pady=(2, 1), sticky="ew") 

    entry_username = CTkEntry(login_frame, font=("Arial", 14, "bold"))
    entry_username.grid(row=1, column=1, padx=10, pady=(1, 5), sticky="ew")  

    label_password = CTkLabel(login_frame, text="Password:", font=("Arial", 12, "bold"))
    label_password.grid(row=2, column=0, padx=5, pady=(2, 1), sticky="ew") 

    entry_password = CTkEntry(login_frame, show='*', font=("Arial", 14, "bold"))
    entry_password.grid(row=2, column=1, padx=10, pady=(1, 5), sticky="ew")  

    label_info = CTkLabel(login_frame, text="", font=("Arial", 13, "bold"), text_color="red")
    label_info.grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky="ew")

    button_login = CTkButton(login_frame, text="Login", command=done)
    button_login.grid(row=4, column=0, columnspan=2, padx=50, pady=5, sticky="ew") 

    login_frame.grid_rowconfigure(0, weight=5)
    login_frame.grid_rowconfigure(1, weight=1)
    login_frame.grid_rowconfigure(2, weight=1)
    login_frame.grid_rowconfigure(3, weight=1)
    login_frame.grid_rowconfigure(4, weight=5)
    login_frame.grid_rowconfigure(5, weight=2)
    login_frame.grid_columnconfigure(0, weight=2)
    login_frame.grid_columnconfigure(1, weight=4)

    root.mainloop()