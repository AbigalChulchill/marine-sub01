import requests
import var_set

token = str(input("please in put your LINE TOKEN = "))

data_base = "/"+"0"+"/"+"0"+"/"+token+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"
requests.post(url=var_set.domain+"/"+"ROBOT_STOP"+data_base)