from mysql.connector import *
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

class Public:
  resultArr = []
  Member = ""
  ID = ""
  
  def sql_connect(self,code,sel):
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_passwd = os.getenv("DB_PASSWD")
    db_name = os.getenv("DB_NAME")
    m1 = connect(user=db_user,passwd=db_passwd,host=db_host,database=db_name)
    c1 = m1.cursor()
    c1.execute(code)
    
    if sel == 1 :
      self.resultArr = c1.fetchall()
    
    m1.commit() 
    c1.close()
    m1.close()
    
  def on_closing(root):
      root.after_cancel("all")
      root.quit()
      Public.ID = "NULL"
      Public.Member = "NULL"
      root.destroy()
  
  def state_disable(self,*args,count=0,pubvar,sel=0):
    if sel == 0:
      word = "disabled"
    else:
      word = "enable"
      
    for i in args:
      try:
        i.insert(0,str(pubvar.resultArr[0][count]))
        i.configure(state=word)
        count += 1
      except Exception:
        pass
          
  def sent_Mail(self,sub,msg,to):    
    subject = sub
    body = msg
    recipient = to
    
    load_dotenv()
    sender = os.getenv("ACC_EMAIL_ID")
    password = os.getenv("ACC_EMAIL_PASSWD")

    message = MIMEMultipart()
    message['From'] = "FISAT Hostel"
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
      with smtplib.SMTP('smtp.gmail.com', 587) as mail:
        mail.ehlo()
        mail.starttls()
        mail.login(sender, password)
        mail.sendmail(sender, recipient, message.as_string())
        mail.close()
        time.sleep(1)

    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email or app password.")
    except Exception as e:
        print("An error occurred:", e)
