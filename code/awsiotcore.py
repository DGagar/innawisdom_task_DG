import time
import logging
import board
import adafruit_dht
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

"""
Generate temperature and humidity data from Raspberry Pi IoT setup
"""

logging.getLogger().setLevel(logging.INFO)

# setup temperature sensor
logging.info('Opening sensor channel')
dhtDevice = adafruit_dht.DHT11(board.D4)

# setup MQTT client
logging.info('Setting up MQTT Client')
myMQTTClient = AWSIoTMQTTClient("ClientID")
myMQTTClient.configureEndpoint("a3fg9pprtcexx2-ats.iot.us-east-1.amazonaws.com", 8883)

logging.info('Authenticating MQTTClient')
myMQTTClient.configureCredentials("/home/pi/AWSIoT/root-ca.pem", "/home/pi/AWSIoT/private.pem.key", "/home/pi/AWSIoT/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # infinite offline publish queueing
myMQTTClient.configureDrainingFrequency(2) # draining 2Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec

logging.info('Initiating IoT Core Topic ...')
myMQTTClient.connect()

while True:
    try:
        # print values to the serial port
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        date_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        logging.info('publishing message from Raspberry Pi {}'.format(date_str))
        myMQTTClient.publish(topic="home/helloworld",QoS=1,payload='{{ "temperature_c": {}, "humidity": {} }}'.format(temperature, humidity))
    except RuntimeError as error:
        pass
    time.sleep(30)
