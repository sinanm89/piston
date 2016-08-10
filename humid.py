#!/usr/local/bin/python
"""Humidity and Temperature sensor"""
import RPi.GPIO as GPIO
import time


def bin2dec(string_num):
    """Turn binary into decimal."""
    return str(int(string_num, 2))


def get_temp_and_hum():
    """Get the temp and hum_bit."""
    data = []

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(4, GPIO.LOW)
    time.sleep(0.02)

    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for i in range(0, 500):
        data.append(GPIO.input(4))

    bit_count = 0
    tmp = 0
    count = 0
    hum_bit = ""
    temp_bit = ""
    crc = ""

    try:
        while data[count] == 1:
            tmp = 1
            count = count + 1 if count < len(data) else count

        for i in range(0, 32):
            bit_count = 0
            while data[count] == 0:
                tmp = 1
                count = count + 1

            while data[count] == 1:
                bit_count = bit_count + 1
                count = count + 1

            if bit_count > 3:
                if i >= 0 and i < 8:
                    hum_bit = hum_bit + "1"
                if i >= 16 and i < 24:
                    temp_bit = temp_bit + "1"
            else:
                if i >= 0 and i < 8:
                    hum_bit = hum_bit + "0"
                if i >= 16 and i < 24:
                    temp_bit = temp_bit + "0"

    except Exception as e:
        print e
        print "ERR_RANGE"
        exit(0)

    try:
        if count > len(data):
            count = count - 1
        for i in range(0, 8):
            bit_count = 0

            while data[count] == 0:
                tmp = 1
                count = count + 1 if count < len(data) else count

            while data[count] == 1:
                bit_count = bit_count + 1
                count = count + 1 if count < len(data) else count

            if bit_count > 3:
                crc = crc + "1"
            else:
                crc = crc + "0"
    except Exception as e:
        print e
        print "ERR_RANGE"
        exit(0)

    hum = bin2dec(hum_bit)
    temp = bin2dec(temp_bit)
    return hum, temp, crc


def main():
    """Main function."""
    try:
        hum, temp, crc = get_temp_and_hum()
    except:
        print 'trying again.'
        return get_temp_and_hum()

    if int(hum) + int(temp) - int(bin2dec(crc)) == 0:
        print "hum_bit: {}%".format(hum)
        print "temp: {}%".format(temp)
    else:
        print 'Hum = {}%'.format(hum)
        print 'temp = {}C'.format(temp)
        print "ERR_CRC"


if __name__ == '__main__':
    main()
