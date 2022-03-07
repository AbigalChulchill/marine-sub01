import requests

token = str(input("please in put your LINE TOKEN = "))

data_base = "/"+"0"+"/"+"0"+"/"+token+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"+"/"+"0"
requests.post(url="https://marine-invest.herokuapp.com//ROBOT_STOP"+data_base)