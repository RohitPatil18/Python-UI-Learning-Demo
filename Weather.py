import socket
import requests

def weather() :
    msg = ""
    try :
        socket.create_connection(("www.google.com",80))
        res = requests.get("https://ipinfo.io")
        data = res.json()
        city = data['city']
        api_address = "http://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city+"&appid=ca7b83b273b1d0fdc60c025038e0d28d"
        res1 = requests.get(api_address)
        wdata = res1.json()
        temp = wdata['main']['temp']
        msg = "You are in "+city+'. Temperature = '+str(temp)+"°C"

    except OSError :
        msg = "Check your internet connection."

    return msg
