import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
print 'led on'
GPIO.output(18, GPIO.HIGH)
time.sleep(10000)
GPIO.output(18,GPIO.LOW)