import subprocess
import time
import Adafruit_DHT
import sys


sensor = Adafruit_DHT.DHT22 
pin = 2 #for DHT sensor
Hora_empieza=22 #indicate the starting time
hora_final=6  #indicate the ending time
tiempo_de_espera=600 #This variable indicates the amount of time, in seconds, that the program waits before restarting the loop.
comando_a_ejecutar="irsend send_once hisense on" 
temperatura_maxima=25.0  #Max temperature
temperatura_minima=24.0  #Min temperature

Flag=False 


while True:
    hora_actual = time.localtime().tm_hour
    sys.stdout = open('/home/YOUR_USER_NAME/temperature_log.txt', 'a') ######################

    if hora_actual >= Hora_empieza or hora_actual < hora_final:
        print('The time is', hora_actual)
        print("inside the time interval")
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
        time.sleep(5)

        print('The temperature is:', temperatura, 'The humidity is:', humedad)
        
        if temperatura >= temperatura_maxima: 
            if Flag==False: 
                subprocess.run(comando_a_ejecutar, shell=True) 
                print('High Temperature. Switch on the AC')
                sys.stdout.close()
                time.sleep(tiempo_de_espera)
                Flag=True 
                
            else:
                print('The AC is already on')
                sys.stdout.close()
                time.sleep(tiempo_de_espera)


        elif temperatura < temperatura_minima: 
            if Flag==True: 
                print('Low Temperature. Switch off the AC')
                subprocess.run(comando_a_ejecutar, shell=True) 
                sys.stdout.close()
                time.sleep(tiempo_de_espera)
                Flag=False 
            else:
                print('The AC is already off')
                sys.stdout.close()
                time.sleep(tiempo_de_espera)
        else:
            print('inside the temperature range')
            sys.stdout.close()
            time.sleep(tiempo_de_espera)

    else:
        if Flag==True:
            print('OUT of time. Switch off the AC')
            subprocess.run(comando_a_ejecutar, shell=True)
            Flag=False 
        print(hora_actual)  
        print('outside the time interval')
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin) 
        print('The temperature is:', temperatura, 'The humidity is:', humedad)
        sys.stdout.close()
        time.sleep(tiempo_de_espera)
