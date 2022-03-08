import requests
import variable

token = str(input("please in put your LINE TOKEN = "))

data_base = "/"+"0"+"/"+"0"+"/"+token+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"
requests.post(url=variable.domain+"/"+"ROBOT_STOP"+data_base)