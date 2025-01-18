import datetime
from tkinter import messagebox
from PUBLIC import *
import customtkinter as ctk

class GPASS:
  name = ""
  dol = ""
  doe = ""
  reason = ""
  stud_id = ""
  status = True
  def __init__(self,name,dol,doe,reason,stud_id):
    self.name = name
    self.dol = dol
    self.doe = doe
    self.reason = reason
    self.stud_id = stud_id
      
  def check_form_validity(self,e1,e2,e3,ta,e5):
    if len(self.name.strip()) == 0:
      e1.configure(border_color = "red")
      self.status = False
    else:
      e1.configure(border_color = "grey")
      
    if len(self.dol.strip()) == 0:
      e2.configure(border_color = "red")
      self.status = False
    else:
      e2.configure(border_color = "grey")
      
    if len(self.doe.strip()) == 0:
      e3.configure(border_color = "red")
      self.status = False
    else:
      e3.configure(border_color = "grey")
      
    if len(self.reason.strip()) == 0:
      ta.configure(border_width=2,border_color="red")
      self.status = False
    else:
      ta.configure(border_color = "grey")
      
    if len(self.stud_id.strip()) == 0:
      e5.configure(border_color = "red")
      self.status = False
    else:
      e5.configure(border_color = "grey")
      
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    today = datetime.datetime.strptime(today,"%d/%m/%Y").date()
    try:
      str = datetime.datetime.strptime(e2.get(),"%d/%m/%Y").date()
      e2.configure(border_color="grey")
    except Exception:
      e2.configure(border_color="red")
      messagebox.showerror('FORM','Invalid Date Given !')
      self.status = False
    
    if str < today:
      e2.configure(border_color="red")
      messagebox.showerror('FORM','Invalid Date !')
      self.status = False
    else:
      e2.configure(border_color="grey")
    
    try:
      today = datetime.datetime.strptime(e3.get(),"%d/%m/%Y").date()
      e3.configure(border_color="grey")
    except Exception:
      e3.configure(border_color="red")
      messagebox.showerror('FORM','Invalid Date Given !')
      self.status = False
      
    if str >= today:
      e3.configure(border_color="red")
      self.status = False
    else:
      e3.configure(border_color="grey")
    
    if self.status == True:
      authentication = Public()
      authentication.sql_connect(f"select count(*) from login where stud_id = '{self.stud_id}'",1)
      if authentication.resultArr[0][0] == 0:
        self.status = False
        e5.delete(0,ctk.END)
        e5.configure(border_color="red",placeholder_text_color = "red",placeholder_text = "Invalid Student ID !")
      else:
        e5.configure(placeholder_text_color = "grey")
      
  def Save_Data(self,e1,e2,e3,ta,e5):
    if self.status == True:
      content = self.dol.split('/')
      content1 = self.doe.split('/')
      save_data = Public()
      
      save_data.sql_connect(f"insert into check_out(stud_id,check_out_date,check_in_date,status,purpose) values('{self.stud_id}','{content[2]}-{content[1]}-{content[0]}','{content1[2]}-{content1[1]}-{content1[0]}',NULL,'{self.reason}')",0)
      
      messagebox.showinfo('GATE PASS','Gate Pass Request sent Successfully !')
      e1.delete(0,ctk.END)
      e2.delete(0,ctk.END)
      e3.delete(0,ctk.END)
      e5.delete(0,ctk.END)
      ta.delete("1.0", ctk.END)
      