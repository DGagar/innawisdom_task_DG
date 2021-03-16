# Interview Task
> Build a serverless application, based on python code (ideally) and on
> AWS. It can do anythin really, the output is not necessarily the point.
> Its more about what you build and how, what services used, what your
> thought process is and what understanding of AWS is. It is up to you
> what you do, however, it would be good to think in the mindset of 
> Innawisdom and what they do and what may be relevant.

# Solution
Overview of the solution is shown in the architecture schematic below.

![alt text](/images/iot_arch.jpg)

Keeping in theme with the previous exercise, input is generated from a 
Raspberry Pi IoT setup.

<img src="/images/iot_setup.jpg" width="150" height="150" />

Workflow is outlined in the following steps:
1. Data is captured from temperature and humidity sensors.
2. MQTT broker is created to publish data in a topic
3. Rule is created to subscribe Lambda to the topic
4. On Lambda activation:
  * Temperature is converted to from Celcius to Fahrenheit
  * Data is uploaded to s3
5. On successful Lambda activation:
  * Publish event to SNS topic
  * Subscribe mobile to topic via SMS

