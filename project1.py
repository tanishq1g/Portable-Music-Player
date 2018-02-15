from mpu6050 import mpu6050
import RPi.GPIO as GPIO
import time
import math
import pyaudio
import numpy as np
GPIO.setmode(GPIO.BCM)#Set GPIO pin numbering
TRIG = 14                                  #Associate pin 23 to TRIG
ECHO = 15 #Associate pin 24 to ECHO
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)
# octaves = [[16.3,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96,27.50,29.14,30.87],[32.70,34.65,36.71,38.89,41.20,43.65,46.25,49.00,51.91,55.00,58.27,61.74],[65.41,69.30,73.42,77.78,82.41,87.31,92.50,98.00,103.8,110.0,116.5,123.5],[130.8,138.6,146.8,155.6,164.8,174.6,185.0,196.0,207.7,220.0,233.1,246.9],[261.6,277.2,293.7,311.1,329.6,349.2,370.0,392.0,415.3,440.0,466.2,493.9],[523.3,554.4,587.3,622.3,659.3,698.5,740.0,784.0,830.6,880.0,932.3,987.8],[1047,1109,1175,1245,1319,1397,1480,1568,1661,1760,1865,1976],[2093,2217,2349,2489,2637,2794,2960,3136,3322,3520,3729,3951],[4186,4435,4699,4978,5274,5588,5920,6272,6645,7040,7459,7902]]

upper_limit = [30.87,61.74,123.5,246.9,493.9,987.8,1976,3951,7902]
lower_limit = [16.35,32.70,65.41,130.8,261.6,523.3,1047,2093,4186]

def read_distance():
    GPIO.output(TRIG, False)                 #Set TRIG as LOW
    # print ("Waitng For Sensor To Settle")
    #time.sleep(2)                            #Delay of 2 seconds
    
    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                 #Set TRIG as LOW
    
    while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse
    
    while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                #Saves the last known time of HIGH pulse

    pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable
    
    
    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
    distance = round(distance, 2)            #Round to two decimal points
    
    if distance > 2 and distance < 400:      #Check whether the distance is within range
        print ("Distance:"),distance - 0.5,("cm")  #Print distance with 0.5 cm calibration
    else:
        print "Out Of Range"                   #display out of range
    return distance

def frequency(d,ll):
    print "checking frequency",
    x1 = 10
    x2 = 50
    if d >= x2 :
        f = lower_limit[ll]
    elif d <= x1:
        f = upper_limit[ll]
    else:
        f = upper_limit[ll] + ((lower_limit[ll] - upper_limit[ll])/(x2 - x1))*(d - x1)
    # f = ((-15.486)*(read_distance()))+571.33       # sine frequency, Hz, may be float
    return f

def volume(x,y,z):
    print "checking volume",
    y -= math.pi/2
    z -= math.pi/2
    per_tilt_x = (x * 180 / math.pi)*0.9
    per_tilt_y = (y * 180 / math.pi)*0.9
    per_tilt_z = (z * 180 / math.pi)*0.9
    # print -1 * per_tilt_y , "percent tilt for volume movement"
    v= -1 * per_tilt_y
    v = v*100 / 67
    if v > 100:
        return 0
    elif v < 0:
        return 100
    else:
        return 100 - v

def octave(x,y,z):
    print "checking octave number",
    y -= math.pi/2
    z -= math.pi/2
    per_tilt_x = (x * 180 / math.pi)*0.9
    per_tilt_y = (y * 180 / math.pi)*0.9
    per_tilt_z = (z * 180 / math.pi)*0.9
    oc = 0
    if (-1*per_tilt_y) < 2.9:
        x -= math.pi
        per_tilt_x = (x * 180 / math.pi)*0.9
        if per_tilt_z < 0:
            print " octave movement : " , -1 * per_tilt_x
            oc = -1 * per_tilt_x
        else:
            print " octave movement : " , per_tilt_x
            oc = per_tilt_x
    else:
        return 4
    if oc < 10 and oc > -10:
        return 4
    elif oc > 10 and oc < 30:
        return 5
    elif oc > 30 and oc < 50:
        return 6
    elif oc > 50:
        return 7
    elif oc < -10 and oc > -50:
        return 3
    elif oc < -50 :
        return 2
    return 4

def play():
    p = pyaudio.PyAudio()
    sensor = mpu6050(0x68)
    
    vol = 1.0     # range [0.0, 1.0]
    fs = 4000       # sampling rate, Hz, must be integer
    duration = 5   # in seconds, may be float
    
    #for i in samples:
    #    print i,"\n"
    
    # play. May repeat with different volume values (if done interactively)
    while(1):
        print "\nstarting"
        data = sensor.get_accel_data()
        r_acc = pow((pow(data["x"],2) + pow(data["y"],2) + pow(data["z"],2)),0.5)
        # print r_acc
        x_angle = math.acos(data["x"]/r_acc)
        y_angle = math.acos(data["y"]/r_acc)
        z_angle = math.acos(data["z"]/r_acc)
        vol = volume(x_angle,y_angle,z_angle)/100
        print vol
        ll = octave(x_angle,y_angle,z_angle)
        print "octave number : " , ll
        f=frequency(read_distance(),ll)
        print f
        # generate samples, note conversion to float32 array
        samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)
        
        stream.write(vol*samples)
        stream.stop_stream()
        stream.close()
    p.terminate()



play()
