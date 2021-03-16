import json
import boto3
import logging
from datetime import datetime

"""
Lambda function to convert temperature from celcius to fahrenheit
and upload to s3
"""

logging.getLogger().setLevel(logging.INFO)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    temperature_c = event['temperature_c']
    temperature_f = convert_temp(temperature_c)
    output = { 
                'temperature_c': temperature_c,
                'temperature_f': temperature_f,
                'humidity': event['humidity']
    }
    
    upload_to_s3(output)
    
    return output
    
def convert_temp(temperature_c):
    logging.info('Converting temperature to Fahrenheit')
    temperature_f = (temperature_c * 9/5) + 32
    return temperature_f
    
def upload_to_s3(output):
    date_str = datetime.now().strftime("%d-%m-%Y")
    datetime_str = datetime.now().strftime("%H%M%S")
    bucket = 'dannys-home-projects'
    prefix = 'iot_sensor/{}/'.format(date_str)
    upload_path = '/tmp/data.json'
    
    with open(upload_path, 'w') as f:
        json.dump(output, f)
        
    logging.info('Uploading to s3')
    s3_client.upload_file(upload_path, bucket, prefix + '{}-data.json'.format(datetime_str))