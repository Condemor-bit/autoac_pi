# autoac_pi

Project to Automate the Air Conditioner with Raspberry Pi. 

![Screenshot from 2023-07-16 14-42-16](https://github.com/Condemor-bit/autoac_pi/assets/119131987/908c55d5-befc-4586-8dc0-3e3a603ff9a6)

This project offers a cost-effective and straightforward solution to control your air conditioner based on a specific time schedule and desired temperature range. With the help of Raspberry Pi, you can easily program your air conditioning system to turn on and off at designated hours, and by setting temperature thresholds, you can maintain the ideal climate without unnecessary energy consumption.

This user-friendly solution aims to simplify your daily routines and enhance your overall comfort with a cost-efficient approach.




### Install dependences:

>sudo apt update && upgrade
>
>sudo apt install python3-pip
>
>sudo pip3 install adafruit-circuitpython
>
>sudo apt install lirc


### Check GPIO:

type in the terminal 

>pinout

![image](https://github.com/Condemor-bit/autoac_pi/assets/119131987/6d6ca952-7855-4fca-96fa-754c9539d6f9)

In my case, I used GPIO 2 for the DHT sensor and GPIO 14 for the IR emitter.

### configure lirc version 0.10.1

![Screenshot from 2023-07-16 14-50-29](https://github.com/Condemor-bit/autoac_pi/assets/119131987/7324f612-02c7-4b98-8ec1-95b2e1c1c36f)
KY-005 emitter

>sudo nano /etc/lirc/lirc_options.conf 

and change the following lines

driver          = default
device          = /dev/lirc0  #if you add sender and reciver IR should be /dev/lirc01

>sudo nano /boot/config.txt

Find the following lines and remove #

#dtoverlay=gpio-ir,gpio_pin=18  #if you add the reciver uncomment and change de GPIO
dtoverlay=gpio-ir-tx,gpio_pin=14


In the next step, you need a conf file of your remote control and add it into lirc. In my case, it is a custom file. I captured the button with a receiver KY-022.

>sudo /etc/init.d/lircd stop
>
>sudo cp /$HOME/hisense.conf /etc/lirc/lircd.conf.d/hisense.conf
>
>sudo /etc/init.d/lircd start
>
>sudo /etc/init.d/lircd status

if everthing is OK, you neeed to see something like this:

![image](https://github.com/Condemor-bit/autoac_pi/assets/119131987/8e9cbce1-d519-45ee-983b-f3608d8963c5)


check if you can turn on your AC. 


>irsend send_once hisense on ## irsend send_once REMOTE_CONTROL BUTTOM 

If it doesn't work, check the distance. If you used a custom remote file, check the code indentation, another potential factor is the power supply. It should provide enough power to the IR emitter.

### Check DHT sensor
![Screenshot from 2023-07-16 14-55-43](https://github.com/Condemor-bit/autoac_pi/assets/119131987/c87ce4f4-2088-4ac1-8035-cdd331175b2e)
DHT 22, temperature and humidity sensor.

The nextstep is to stay sure that DHT sensor is working. for that make the test file or copy from the repository.

>cd $HOME
>nano test_dht.py


>import Adafruit_DHT
>
>sensor = Adafruit_DHT.DHT22 #specify  DHT22 sensor
>
>pin = 2  # were you connected the sensor
>
>humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
>
>print('The temperature is:', temperatura)
>
>print('The humidity is:', humedad)

Save the file anda type

>python3 test_dht.py

if works you should see 

>The temperature is: 26.600000381469727
>
>The humidity is: 47.099998474121094

### Configure the automation script

Copy the Temperature_control.py file to your home directory.

>cd $HOME
>
>nano Temperature_control.py

and modfy the folloing lines for your proupose

>sensor = Adafruit_DHT.DHT22
>
>pin = 2 #for DHT sensor
>
>Hora_empieza=22 #indicate the starting time
>
>hora_final=6  #indicate the ending time
>
>tiempo_de_espera=600 #This variable indicates the amount of time, in seconds, that the program waits before restarting the loop.
>
>comando_a_ejecutar="irsend send_once hisense on"
>
>temperatura_maxima=25.0  #Max temperature
>
>temperatura_minima=24.0  #Min temperature


Also, replace YOUR_USER_NAME with your actual username in the line:

>sys.stdout = open('/home/YOUR_USER_NAME/temperature_log.txt', 'a')

Save and close the file.

Now is necesary add the script to crontab. Crontab is a scheduling tool to automate tasks at predefined times in Unix-based systems. 

>crontab -e

The first time you run this command, it will ask you to specify the editor. Choose option 1 and add the following line at the end:

>@reboot python3 $HOME/Temperature_control.py >> $HOME/temperature_log.txt 2>&1

Save and exit the crontab editor.

This line ensures that your script runs on every Raspberry Pi reboot. Additionally, you can check the log and the output of the script by typing:
>cat temperature_log.txt

To initialize the script upon system startup, type 

>sudo reboot



Enjoy this simple and smart climatization solution
