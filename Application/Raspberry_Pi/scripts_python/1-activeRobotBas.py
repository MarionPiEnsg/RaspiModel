import RPi.GPIO as GPIO
import time
import sys

servo_pin = 11
duty_cycle = float(sys.argv[1])     

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM channel on the servo pin with a frequency of 50Hz
pwm_servo = GPIO.PWM(servo_pin, 50)
pwm_servo.start(duty_cycle)

try:
    while True:
        pwm_servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.01)
        GPIO.cleanup()
        exit()
except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")


