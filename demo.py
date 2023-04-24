import pi_servo_hat
import time

# Initialize Constructor
steer = pi_servo_hat.PiServoHat()
steer.restart()

steer.move_servo_position(0, 0)

# +28 degrees is straight ahead
while(True):
    angle = int(input("Enter angle: "))
    tic = time.perf_counter()
    if (angle > -45 and angle < 45):
        steer.move_servo_position(0, angle+28)
    else:
        print("Sorry, angle invalid. Pick a number on the range [-45, 45]")
    
    toc = time.perf_counter()
    print(f"Finished in {toc - tic:0.4f} seconds")