import pi_servo_hat
import time

# Initialize Constructor
steer = pi_servo_hat.PiServoHat()
steer.restart()

steer.move_servo_position(0, 0)

def set_angle():
    angle = int(input("Enter angle: "))
    tic = time.perf_counter()
    if (angle > -46 and angle < 46):
        steer.move_servo_position(0, angle+28)
        # +28 degrees is straight ahead
    else:
        print("Sorry, angle invalid. Pick a number on the range [-45, 45]")
def set_speed():
    pass

# +28 degrees is straight ahead
while(True):
    tic = time.perf_counter()
    # main code goes here
    set_angle()
    toc = time.perf_counter()
    print(f"Finished in {toc - tic:0.4f} seconds")

