from __future__ import print_function
import pi_servo_hat
import time
import sys
import math
import qwiic_scmd
import qwiic_dual_encoder_reader
#import acconeer.exptool as et #library for radar module

# The first two I2C channels
# 0x5D
motors = qwiic_scmd.QwiicScmd()
# Initialize Constructor
steer = pi_servo_hat.PiServoHat()
steer.restart()

DECAY = 0.0003
R_MTR = 0
L_MTR = 1
if (dir):
    # set forward
    FWD = 0
    BWD = 1
else:
    # set reverse
    FWD = 1
    BWD = 0   
SLEEP = 0.1
speed_min = 20
speed_max = 250
ticks_per_rev = 9.7*48
wheel_radius = 3.25
TURN_TICKS = 250

if motors.connected == False:
    print("Motor Driver not connected. Check connections.", \
        file=sys.stderr)
    sys.exit(0)
motors.begin()
time.sleep(.250)

# Zero Motor Speeds
motors.set_drive(0,0,0)
motors.set_drive(1,0,0)

motors.enable()
print("Motor enabled")
time.sleep(.250)

myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
myEncoders.begin()

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

def set_speed(distance: float, speed: int, dir: bool):
    myEncoders.count1 = 0
    target = ((distance/100)*ticks_per_rev)/(2*math.pi*(wheel_radius/100))
    #print(abs(target))
    while(abs(myEncoders.count1) < target - target/5): #- target/5
        motors.set_drive(L_MTR,FWD,speed)
        motors.set_drive(R_MTR,BWD,speed)
        time.sleep(0.05)
        print(abs(myEncoders.count1))    
    motors.disable()
    
def turn_left(speed: int, angle: int):
    set_angle(angle)
    time.sleep(1)
    motors.enable()
    myEncoders.count1 = 0
    # arbitrary value to get to a 90 degree turn
    target = TURN_TICKS
    while(abs(myEncoders.count1) < target): #- target/5
        # help the turn by reducing one motor
        motors.set_drive(L_MTR,FWD,speed/2)
        motors.set_drive(R_MTR,BWD,speed)
        time.sleep(0.05)
        print(abs(myEncoders.count1))  
        # reset to straight ahead
    set_angle(0)
    motors.disable()

def turn_right(speed: int, angle: int):
    set_angle(angle)
    time.sleep(1)
    motors.enable()   
    myEncoders.count2 = 0
    # arbitrary value to get to a 90 degree turn
    target = TURN_TICKS
    # CHANGE TO count2 BECAUSE RIGHT MOTOR
    while(abs(myEncoders.count2) < target): #- target/5
        # help the turn by reducing one motor
        motors.set_drive(L_MTR,FWD,speed)
        motors.set_drive(R_MTR,BWD,speed/2)
        time.sleep(0.05)
        print(abs(myEncoders.count1))  
        # reset to straight ahead
    set_angle(0)
    motors.disable()
    


    # i = 0
    # while (myEncoders.count1 < target):
    #     if(speed > speed * 0.3):
    #         speed_norm = speed_norm*math.exp(-DECAY*i)
    #         speed = (speed_max - speed_min)*speed_norm + speed_min
    #         speed = int(speed)
    #         i = i + 1
    #     motors.set_drive(L_MTR,FWD,speed)
    #     motors.set_drive(R_MTR,BWD,speed)
    #     time.sleep(0.05)
    #     print(abs(myEncoders.count1))      

        

    motors.disable()
# +28 degrees is straight ahead
def program():
    #tic = time.perf_counter()
    # main code goes here
    # set_angle(-45)
    # time.sleep(1)
    set_angle(0)
    time.sleep(1)
    set_speed(distance=35, speed=70, dir=True)
    time.sleep(1)
    turn_left(speed=50, angle=-45)
    turn_right(speed=50, angle=45)
    #toc = time.perf_counter()
    #print(f"Finished in {toc - tic:0.4f} seconds")

if __name__ == '__main__':
	try:
		program()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("Ending demo.py")
		motors.disable()
		sys.exit(0)
