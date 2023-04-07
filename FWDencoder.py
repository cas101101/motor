from __future__ import print_function
import time
import sys
import math
import qwiic_scmd
import qwiic_dual_encoder_reader

myMotor = qwiic_scmd.QwiicScmd()

def runExample(revs: float):
    tic = time.perf_counter()
    print("Motor Test.")
    DECAY = 0.0003
    R_MTR = 0
    L_MTR = 1
    FWD = 0
    BWD = 1
    SLEEP = 0.1
    speed_min = 20
    speed_max = 250
    ticks_per_rev = 9.7*48
    
    if myMotor.connected == False:
        print("Motor Driver not connected. Check connections.", \
            file=sys.stderr)
        return
    myMotor.begin()
    print("Motor initialized.")
    time.sleep(.250)

    # Zero Motor Speeds
    myMotor.set_drive(0,0,0)
    myMotor.set_drive(1,0,0)

    myMotor.enable()
    print("Motor enabled")
    time.sleep(.250)
    
    myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
    print("here1")
    myEncoders.begin()
    print("here2")
    myEncoders.count1 = 0
    print("here3")
    speed = 150
    target =  ticks_per_rev*revs
    i = 0
    #normalize the speed
    speed_norm = (speed - speed_min)/(speed_max - speed_min)
    print("here4")
    start_speed = 0.3*speed
    while (myEncoders.count1 < ticks_per_rev):
        if(start_speed < speed):
            start_speed = 0.01*start_speed*math.exp(DECAY*i)
            i = i + 1
        myMotor.set_drive(R_MTR,FWD,start_speed)
    
    while(myEncoders.count1 < target - target/5): 
        myMotor.set_drive(R_MTR,FWD,speed)
        
    while (myEncoders.count1 < target):
        if(speed > speed * 0.3):
            speed_norm = speed_norm*math.exp(-DECAY*i)
            speed = (speed_max - speed_min)*speed_norm + speed_min
            i = i + 1
        myMotor.set_drive(R_MTR,FWD,speed)
    toc = time.perf_counter()
    print(f"Finished in {toc - tic:0.4f} seconds")
    myMotor.disable()

    






if __name__ == '__main__':
    try:
        runExample(1)

    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)
