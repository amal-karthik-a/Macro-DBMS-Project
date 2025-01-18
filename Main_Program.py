from login import *
import home
from Warden_home import *

while Public.Member == "" and Public.ID == "":  
  
  main_login()
  if Public.Member == "S":
    home.home_student_dash()
  elif Public.Member == "W":
    home_warden_dash()