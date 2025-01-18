import customtkinter as ctk
from PUBLIC import *
from LeavE_ForM import *
from datetime import *
from feedback import *

def load_data(id_load):
    global Public_inst
    Public_inst = Public()
    Public_inst.sql_connect(f"select * from student where stud_id='{id_load}'", 1)

def show_fees_content():
    for widget in right_frame.winfo_children():
        widget.destroy()

    button_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    button_frame.pack(pady=(20, 10))

    # "Fee Due" button
    fee_due_button = ctk.CTkButton(button_frame, text="Fee Due", command=show_fee_due, width=200, height=40, font=("Poppins", 14))
    fee_due_button.grid(row=0, column=0, padx=10, pady=10)
    
    pay_fee_button = ctk.CTkButton(button_frame, text="Pay Fee", command=show_pay_fee, width=200, height=40, font=("Poppins", 14))
    pay_fee_button.grid(row=0, column=1, padx=10, pady=10)

    global content_frame
    content_frame = ctk.CTkFrame(right_frame, fg_color="#393939", border_width=2, border_color="#826A6A")
    content_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    show_fee_due()

def show_fee_due():
    public_var1 = Public()
    code = f"select rent,mess,(rent+mess), due_date,status from fee where stud_id = '{Public.ID}'"
    public_var1.sql_connect(code,1)
    
    print(public_var1.resultArr)
    
    for widget in content_frame.winfo_children():
        widget.destroy()

    content_label = ctk.CTkLabel(content_frame, text="Fee Due Details", font=("Arial", 20, "bold"))
    content_label.pack(pady=(10, 5))
    
    fee_details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    fee_details_frame.pack(pady=5, padx=20, anchor="center", fill="x")
    
    hostel_fee_label = ctk.CTkLabel(fee_details_frame, text="Hostel Fee:", font=("Arial", 16, "bold"))
    hostel_fee_label.grid(row=0, column=0, sticky="w", padx=(200, 5), pady=(5, 2))
    hostel_fee_entry = ctk.CTkEntry(fee_details_frame, width=200, font=("Arial", 14))
    hostel_fee_entry.grid(row=0, column=1, pady=(5, 2), padx=(0, 10))

    mess_fee_label = ctk.CTkLabel(fee_details_frame, text="Mess Fee:", font=("Arial", 16, "bold"))
    mess_fee_label.grid(row=1, column=0, sticky="w", padx=(200, 5), pady=(5, 2))
    mess_fee_entry = ctk.CTkEntry(fee_details_frame, width=200, font=("Arial", 14))
    mess_fee_entry.grid(row=1, column=1, pady=(5, 2), padx=(0, 10))

    total_fee_label = ctk.CTkLabel(fee_details_frame, text="Total Fee:", font=("Arial", 16, "bold"))
    total_fee_label.grid(row=2, column=0, sticky="w", padx=(200, 5), pady=(5, 2))
    total_fee_entry = ctk.CTkEntry(fee_details_frame, width=200, font=("Arial", 14))
    total_fee_entry.grid(row=2, column=1, pady=(5, 2), padx=(0, 10))

    due_date_label = ctk.CTkLabel(fee_details_frame, text="Due Date:", font=("Arial", 16, "bold"))
    due_date_label.grid(row=3, column=0, sticky="w", padx=(200, 5), pady=(5, 2))
    due_date_entry = ctk.CTkEntry(fee_details_frame, width=200, font=("Arial", 14))
    due_date_entry.grid(row=3, column=1, pady=(5, 2), padx=(0, 10))
    
    Status_Label = ctk.CTkLabel(fee_details_frame, text="Status:", font=("Arial", 16, "bold"))
    Status_Label.grid(row=4, column=0, sticky="w", padx=(200, 5), pady=(5, 2))
    Status_Entry = ctk.CTkEntry(fee_details_frame, width=200, font=("Arial", 14))
    Status_Entry.grid(row=4, column=1, pady=(5, 2), padx=(0, 10))
    
    public_var1.state_disable(hostel_fee_entry,mess_fee_entry,total_fee_entry,due_date_entry,Status_Entry,count=0,pubvar=public_var1,sel=0)
    
    fee_details_frame.grid_columnconfigure(0, weight=1)
    fee_details_frame.grid_columnconfigure(1, weight=1)

def show_pay_fee():
    # Clear the content frame and display Pay Fee content
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    content_label = ctk.CTkLabel(content_frame, text="Pay Fee", font=("Arial", 20, "bold"))
    content_label.pack(pady=(10, 20))
    
    pay_fee_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    pay_fee_frame.pack(pady=5, padx=20, anchor="center", fill="x")

    # Display Total Amount Due
    amount_due_label = ctk.CTkLabel(pay_fee_frame, text="Total Amount Due:", font=("Arial", 16, "bold"))
    amount_due_label.grid(row=0, column=0, sticky="w", padx=(200, 5), pady=(5, 10))
    amount_due_entry = ctk.CTkEntry(pay_fee_frame, width=200, font=("Arial", 14))
    amount_due_entry.grid(row=0, column=1, pady=(5, 10), padx=(0, 10))
    amount_due_entry.insert(0, "Amount Placeholder")
    amount_due_entry.configure(state='disabled')

    payment_method_label = ctk.CTkLabel(pay_fee_frame, text="Payment Method:", font=("Arial", 16, "bold"))
    payment_method_label.grid(row=1, column=0, sticky="w", padx=(200, 5), pady=(5, 10))
    
    payment_method_var = ctk.StringVar(value="Credit Card")
    credit_card_rb = ctk.CTkRadioButton(pay_fee_frame, text="Credit Card", variable=payment_method_var, value="Credit Card")
    credit_card_rb.grid(row=1, column=1, sticky="w")
    debit_card_rb = ctk.CTkRadioButton(pay_fee_frame, text="Debit Card", variable=payment_method_var, value="Debit Card")
    debit_card_rb.grid(row=1, column=2, sticky="w")
    net_banking_rb = ctk.CTkRadioButton(pay_fee_frame, text="Net Banking", variable=payment_method_var, value="Net Banking")
    net_banking_rb.grid(row=1, column=3, sticky="w")

    # Card/Account Details
    account_label = ctk.CTkLabel(pay_fee_frame, text="Card/Account Number:", font=("Arial", 16))
    account_label.grid(row=2, column=0, sticky="w", padx=(200, 5), pady=(10, 10))
    account_entry = ctk.CTkEntry(pay_fee_frame, width=200, font=("Arial", 14))
    account_entry.grid(row=2, column=1, pady=(10, 10), padx=(0, 10))

    # CVV for cards
    cvv_label = ctk.CTkLabel(pay_fee_frame, text="CVV:", font=("Arial", 16))
    cvv_label.grid(row=3, column=0, sticky="w", padx=(200, 5), pady=(10, 10))
    cvv_entry = ctk.CTkEntry(pay_fee_frame, width=80, font=("Arial", 14), show="*")
    cvv_entry.grid(row=3, column=1, pady=(10, 10), padx=(0, 10))

    # Expiry Date for cards
    expiry_label = ctk.CTkLabel(pay_fee_frame, text="Expiry Date (MM/YY):", font=("Arial", 16))
    expiry_label.grid(row=4, column=0, sticky="w", padx=(200, 5), pady=(10, 10))
    expiry_entry = ctk.CTkEntry(pay_fee_frame, width=80, font=("Arial", 14))
    expiry_entry.grid(row=4, column=1, pady=(10, 10), padx=(0, 10))

    # Pay Button
    pay_button = ctk.CTkButton(pay_fee_frame, text="Pay Now", command=confirm_payment, width=150, height=40, font=("Poppins", 14, "bold"), fg_color="#4CAF50", hover_color="#388E3C")
    pay_button.grid(row=5, column=0, columnspan=3, pady=(20, 10))

    # Arrange grid columns
    pay_fee_frame.grid_columnconfigure(0, weight=1)
    pay_fee_frame.grid_columnconfigure(1, weight=1)
    pay_fee_frame.grid_columnconfigure(2, weight=1)

def confirm_payment():
    for widget in content_frame.winfo_children():
        widget.destroy()

    success_label = ctk.CTkLabel(content_frame, text="Payment Successful", font=("Arial", 20, "bold"), fg_color="green")
    success_label.pack(pady=20)

def FB_FUN():
    for widget in right_frame.winfo_children():
        widget.destroy()
    main_USER_FB(right_frame)

def show_profile_content():
    for widget in right_frame.winfo_children():
        widget.destroy()
    
    load_data(Public.ID)
    
    title_label = ctk.CTkLabel(right_frame, text="Student Profile", font=("Arial", 20, "bold"))
    title_label.pack(pady=(20, 10))

    # Personal Details Section
    personal_frame = ctk.CTkFrame(right_frame)
    personal_frame.pack(fill="x", padx=10, pady=10)

    personal_title = ctk.CTkLabel(personal_frame, text="Personal Details", font=("Arial", 16, "bold"))
    personal_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Left side of Personal Section
    left_personal_frame = ctk.CTkFrame(personal_frame, fg_color="transparent")
    left_personal_frame.grid(row=1, column=0, sticky="nsew", padx=10)

    ctk.CTkLabel(left_personal_frame, text="Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
    name_entry = ctk.CTkEntry(left_personal_frame, width=200)
    name_entry.grid(row=1, column=0, pady=5)
    name_entry.insert(0,(Public_inst.resultArr[0][1]+"   "+Public_inst.resultArr[0][2]))
    name_entry.configure(state='disabled')

    ctk.CTkLabel(left_personal_frame, text="Date of Birth:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=5)
    dob_entry = ctk.CTkEntry(left_personal_frame, width=200)
    dob_entry.grid(row=3, column=0, pady=5)

    ctk.CTkLabel(left_personal_frame, text="Contact:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", pady=5)
    cont_stud_entry = ctk.CTkEntry(left_personal_frame, width=200)
    cont_stud_entry.grid(row=5, column=0, pady=5)

    # Right side of Personal Section
    right_personal_frame = ctk.CTkFrame(personal_frame, fg_color="transparent")
    right_personal_frame.grid(row=1, column=1, sticky="nsew", padx=10)

    ctk.CTkLabel(right_personal_frame, text="Email:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
    email_entry = ctk.CTkEntry(right_personal_frame, width=200)
    email_entry.grid(row=1, column=0, pady=5)

    ctk.CTkLabel(right_personal_frame, text="Gender:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=5)
    gender_entry = ctk.CTkEntry(right_personal_frame, width=200)
    gender_entry.grid(row=3, column=0, pady=5)

    ctk.CTkLabel(right_personal_frame, text="Age:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", pady=5)
    age_entry = ctk.CTkEntry(right_personal_frame, width=200)
    age_entry.grid(row=5, column=0, pady=5)

    # Parents Section
    parents_frame = ctk.CTkFrame(right_frame)
    parents_frame.pack(fill="x", padx=10, pady=10)

    parents_title = ctk.CTkLabel(parents_frame, text="Parents Details", font=("Arial", 16, "bold"))
    parents_title.grid(row=0, column=0, columnspan=6, pady=10)

    ctk.CTkLabel(parents_frame, text="Father's Name:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
    father_entry = ctk.CTkEntry(parents_frame, width=100)
    father_entry.grid(row=2, column=0, padx=(10, 0), pady=5)

    ctk.CTkLabel(parents_frame, text="Mother's Name:", font=("Arial", 14)).grid(row=1, column=1, sticky="w", pady=5)
    mother_entry = ctk.CTkEntry(parents_frame, width=100)
    mother_entry.grid(row=2, column=1, padx=(10, 0), pady=5)

    ctk.CTkLabel(parents_frame, text="Parent's Contact:", font=("Arial", 14)).grid(row=1, column=2, sticky="w", pady=5)
    contact_entry = ctk.CTkEntry(parents_frame, width=100)
    contact_entry.grid(row=2, column=2, padx=(10, 0), pady=5)

    for i in range(3):
        parents_frame.grid_columnconfigure(i, weight=1)

    # Location Section
    location_frame = ctk.CTkFrame(right_frame)
    location_frame.pack(fill="x", padx=10, pady=10)

    location_title = ctk.CTkLabel(location_frame, text="Location Details", font=("Arial", 16, "bold"))
    location_title.grid(row=0, column=0, columnspan=2, pady=10)

    ctk.CTkLabel(location_frame, text="Address:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
    address_entry = ctk.CTkEntry(location_frame, width=250)
    address_entry.grid(row=2, column=0, padx=(10, 0), pady=5)

    ctk.CTkLabel(location_frame, text="Room No:", font=("Arial", 14)).grid(row=1, column=1, sticky="w", pady=5)
    room_entry = ctk.CTkEntry(location_frame, width=100)
    room_entry.grid(row=2, column=1, padx=(10, 0), pady=5)

    # Academic Section
    academic_frame = ctk.CTkFrame(right_frame)
    academic_frame.pack(fill="x", padx=10, pady=10)

    academic_title = ctk.CTkLabel(academic_frame, text="Academic Details", font=("Arial", 16, "bold"))
    academic_title.grid(row=0, column=0, columnspan=6, pady=10)

    # First row: Roll No, Class, Section
    ctk.CTkLabel(academic_frame, text="Roll No:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
    roll_entry = ctk.CTkEntry(academic_frame, width=100)
    roll_entry.grid(row=2, column=0, padx=(10, 0), pady=5)

    ctk.CTkLabel(academic_frame, text="Class:", font=("Arial", 14)).grid(row=1, column=1, sticky="w", pady=5)
    class_entry = ctk.CTkEntry(academic_frame, width=100)
    class_entry.grid(row=2, column=1, padx=(10, 0), pady=5)

    ctk.CTkLabel(academic_frame, text="Section:", font=("Arial", 14)).grid(row=1, column=2, sticky="w", pady=5)
    section_entry = ctk.CTkEntry(academic_frame, width=100)
    section_entry.grid(row=2, column=2, padx=(10, 0), pady=5)

    # Second row: Remark, Passout Year, Admission Year
    ctk.CTkLabel(academic_frame, text="Remark:", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=5)
    remark_entry = ctk.CTkEntry(academic_frame, width=100)
    remark_entry.grid(row=4, column=0, padx=(10, 0), pady=5)
    
    ctk.CTkLabel(academic_frame, text="Passout Year:", font=("Arial", 14)).grid(row=3, column=1, sticky="w", pady=5)
    passout_year_entry = ctk.CTkEntry(academic_frame, width=100)
    passout_year_entry.grid(row=4, column=1, padx=(10, 0), pady=5)

    ctk.CTkLabel(academic_frame, text="Admission Year:", font=("Arial", 14)).grid(row=3, column=2, sticky="w", pady=5)
    admission_no = ctk.CTkEntry(academic_frame, width=100)
    admission_no.grid(row=4, column=2, padx=(10, 0), pady=5)

    for i in range(3):
        academic_frame.grid_columnconfigure(i, weight=1)
    Public_inst.state_disable(email_entry,cont_stud_entry,address_entry,passout_year_entry,room_entry,mother_entry,father_entry,contact_entry,remark_entry,dob_entry,gender_entry,class_entry,section_entry,roll_entry,admission_no,count=3,pubvar=Public_inst,sel=0)
    
    today = date.today()
    dob = datetime.strptime(dob_entry.get(), "%Y-%m-%d").date()
    b = divmod((today - dob).days,365)
    age_entry.insert(0,str(b[0]))

def center_window(window, width=1350, height=950):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    
def show_content(content):
    for widget in right_frame.winfo_children():
        widget.destroy()
    content_label = ctk.CTkLabel(right_frame, text=content, font=("Arial", 20))
    content_label.pack(pady=20)

def logout():
    Public.Member = ""
    Public.ID = ""
    app_stud.destroy() 

def home_student_dash():
    global app_stud, bottom_frame, right_frame, upper_frame
    app_stud = ctk.CTk()
    app_stud.geometry("1350x950")
    app_stud.title("Student Dashboard")
    app_stud.configure(fg_color="#1E1E1E")

    center_window(app_stud)
    left_frame = ctk.CTkFrame(app_stud, width=300, fg_color="transparent")
    left_frame.pack(side="left", fill="y", padx=20, pady=20)

    # Upper frame for profile details
    upper_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    upper_frame.pack(fill="x", padx=10, pady=(10, 5))

    # Date label in the upper frame
    date_label = ctk.CTkLabel(upper_frame, text=f"Date : {date.today()}", font=("Arial", 12))
    date_label.pack(anchor="w", padx=5, pady=(10, 5))

    # Enlarged Student label
    student_label = ctk.CTkLabel(upper_frame, text="STUDENT", font=("Monoton", 24, "bold"))
    student_label.pack(pady=(10, 5))

    bottom_frame = ctk.CTkFrame(left_frame, fg_color="#2F2C2C")
    bottom_frame.pack(fill="x", expand=True, padx=10, pady=(5, 10))

    buttons = {
        "Profile": lambda: show_profile_content(),
        "Fees": lambda: show_fees_content(),
        "Gate Pass": lambda: Gate_con(right_frame),
        "Feedback": lambda: FB_FUN()
    }

    for text, command in buttons.items():
        btn = ctk.CTkButton(bottom_frame, text=text, command=command, width=260, height=40, fg_color="#393939", hover_color="#938989", font=("Poppins", 15, "bold"))
        btn.pack(pady=10, padx=20)

    logout_button = ctk.CTkButton(bottom_frame, text="Log Out", command=logout, fg_color="red", width=260, height=40, font=("Poppins", 13, 'bold'))
    logout_button.pack(pady=(30, 20), padx=20)

    right_frame = ctk.CTkFrame(app_stud, corner_radius=10, width=900, height=850, border_width=2, border_color="#826A6A", fg_color="#2F2C2C")
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    
    app_stud.mainloop()
