import os
import time
import requests
import webbrowser
import urllib.request
import thingspeak
import psutil

def getFree():
    free = os.popen("free -h")
    i = 0
    while True:
        i = i + 1
        line = free.readline()
        if i==2:
            return(line.split()[0:7])


def temp_gpu():
    gpu_temp = os.popen("vcgencmd measure_temp").readline()
    os.close
    gpu_temp=gpu_temp.replace("'C", "")
    gpu_temp=gpu_temp.replace("temp=", "")
    return gpu_temp
 
def temp_cpu():
    
    with open(r"/sys/class/thermal/thermal_zone0/temp") as File:
        cpu_temp = File.readline()
        os.close

    cpu_temp=round(float(cpu_temp)/1000, 1)
    return cpu_temp

write_key='7W0Z4EY9E6UTQUYV'
channel_id=1727808

if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, api_key=write_key)
    try:   
        while True:
            requisicao=requests.get('https://thingspeak.com/channels/1727808/fields/1/last?key=WHI8CNL64M2073N2')
            print("Valor lido:" + requisicao.text)
            if requisicao.text == "1":
                print("enviar")
               
                a=temp_gpu()
                b=temp_cpu()
                load=psutil.cpu_percent()
                
                mem = getFree()
                mem[2]=mem[2].replace("Mi","")
                mem[3]=mem[3].replace("Gi","")

                memory=(float(mem[2])/1000)/float(mem[3])*100
                
                print(a)
                print(b)
                
                response=channel.update({'field2': float(a),'field3': b, 'field4':load, 'field5':memory})
                
            else:
                print("não enviar")
            time.sleep(15)
    except:
        print("erro de coneção")
