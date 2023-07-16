# autoac_pi

```Project to Automate the Air Conditioner with Raspberry Pi. Step by step.

### Install dependences:


>sudo apt update && upgrade
>sudo apt install python3-pip
>sudo pip3 install adafruit-circuitpython
>sudo apt install lirc


### Check GPIO:

>pinout

![image](https://github.com/Condemor-bit/autoac_pi/assets/119131987/6d6ca952-7855-4fca-96fa-754c9539d6f9)

In my case, I used GPIO 2 for the DHT sensor and GPIO 14 for the IR emitter.

### configure lirc version 0.10.1

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
>sudo cp /$HOME/hisense.conf /etc/lirc/lircd.conf.d/hisense.conf
>sudo /etc/init.d/lircd start
>sudo /etc/init.d/lircd status

if everthing is OK, you neeed to see something like this:

![image](https://github.com/Condemor-bit/autoac_pi/assets/119131987/8e9cbce1-d519-45ee-983b-f3608d8963c5)


check if you can turn on your AC. 


>irsend send_once hisense on ## irsend send_once REMOTE_CONTROL BUTTOM 

If it doesn't work, check the distance. If you used a custom remote file, check the code indentation, and the power supply. It should provide enough power to the IR emitter.

### Configurationtemperature and humidity sensor

The nextstep is to stay sure that DHT sensor is working. for that make the test file 

>nano test_dht.py


>import Adafruit_DHT
>
>sensor = Adafruit_DHT.DHT22 #specify  DHT22 sensor
>pin = 2  # were you connected the sensor
>
>humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
>
>print('The temperature is:', temperatura)
>print('The humidity is:', humedad)

Save the file anda type

>python3 test_dht.py

if works you should see 

>The temperature is: 26.600000381469727
>The humidity is: 47.099998474121094




Under construction
