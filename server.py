from flask import Flask

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

app = Flask(__name__)
application = app


@app.route('/up/<seconds>')
def go_up(seconds):
    """Endpoint for the table to go up."""
    seconds = int(seconds)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(17, GPIO.LOW)
    return '<a href="up/{0}">Go up {1} seconds again</a>'.format(
        seconds, seconds)


@app.route('/down/<seconds>')
def go_down(seconds):
    """Endpoint for the table to go down."""
    seconds = int(seconds)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(27, GPIO.LOW)
    return '<a href="up/{0}">Go up {1} seconds again</a>'.format(
        seconds, seconds)


@app.route('/')
def index():
    """Default view options for piston."""
    seconds_up = seconds_down = 5
    g_up = '<a href="up/{0}">Go up {1} seconds</a>'.format(
        seconds_up, seconds_up)
    g_down = '<a href="down/{0}">Go up {1} seconds</a>'.format(
        seconds_down, seconds_down)
    return '<h1>{0}</h1><ul><li>{1}</li/><li>{2}</li></ul>'.format(
        'Raise/Lower table', g_up, g_down)
