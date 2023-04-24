from __future__ import print_function
import pi_servo_hat
import time
import sys
import math
import qwiic_scmd
import qwiic_dual_encoder_reader

# The first two I2C channels
# 0x5D
left = qwiic_scmd.QwiicScmd()
#right = qwiic_scmd.QwiicScmd(0x58)
# Initialize Constructor
steer = pi_servo_hat.PiServoHat()
steer.restart()

# start straight ahead
steer.move_servo_position(0, 28)
print("Init done")
def set_angle(angle: float):
    #angle = int(input("Enter angle: "))
    #tic = time.perf_counter()
    if (angle > -46 and angle < 46):
        steer.move_servo_position(0, angle+28)
        # +28 degrees is straight ahead
    else:
        print("Sorry, angle invalid. Pick a number on the range [-45, 45]")

def set_speed(distance: float, speed: float, dir: bool):
    DECAY = 0.0003
    R_MTR = 0
    L_MTR = 1
    if (dir):
        # set forward
        FWD = 0
    else:
        # set reverse
        FWD = 1   
    SLEEP = 0.1
    speed_min = 20
    speed_max = 250
    ticks_per_rev = 9.7*48
    wheel_radius = 3.25
    
    if left.connected == False:
        print("Motor Driver not connected. Check connections.", \
            file=sys.stderr)
        return
    left.begin()
    #right.begin()
    time.sleep(.250)

    # Zero Motor Speeds
    left.set_drive(0,0,0)
    left.set_drive(1,0,0)
    #right.set_drive(0,0,0)
    #right.set_drive(1,0,0)

    left.enable()
    print("Motor enabled")
    time.sleep(.250)
    
    myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
    myEncoders.begin()
    myEncoders.count1 = 0
    speed = 250
    target = ((distance/100)*ticks_per_rev)/(2*math.pi*(wheel_radius/100))
    print(target)
    print(myEncoders.count1)
    left.set_drive(L_MTR,FWD,speed)
    time.sleep(5)
    print("done with drive")
    i = 0
    # normalize the speed
    speed_norm = (speed - speed_min)/(speed_max - speed_min)
    while(myEncoders.count1 < target - target/5): #- target/5
        left.set_drive(L_MTR,FWD,speed)
        #right.set_drive(R_MTR,FWD,speed)
        
    while (myEncoders.count1 < target):
        if(speed > speed * 0.3):
            speed_norm = speed_norm*math.exp(-DECAY*i)
            speed = (speed_max - speed_min)*speed_norm + speed_min
            i = i + 1
        left.set_drive(L_MTR,FWD,speed)
        #right.set_drive(R_MTR,FWD,speed)
    left.disable()
    #right.disable()

# +28 degrees is straight ahead
while(True):
    #tic = time.perf_counter()
    # main code goes here
    set_angle(-45)
    time.sleep(4)
    set_angle(45)
    time.sleep(4)
    set_speed(30, 150, True)
    #toc = time.perf_counter()
    #print(f"Finished in {toc - tic:0.4f} seconds")

