import RPi.GPIO as GPIO
import time
import sys

#on renseigne le pin sur lequel est branché le cable de commande du servo moteur inférieur (droite-gauche)
servo_pin = 11
#recuperation de la valeur du mouvement a envoyer au servo
duty_cycle = float(sys.argv[1])     

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

# Creation du cannal PWM sur le servo pin avec une frequence de 50Hz
pwm_servo = GPIO.PWM(servo_pin, 50)
pwm_servo.start(duty_cycle)

try:
    while True:
        pwm_servo.ChangeDutyCycle(duty_cycle) #le servo se pivote avec la valeur donnee en entree
        time.sleep(0.01) # on attend un petit moment que le servo finisse son action
        GPIO.cleanup() # on sort proprement de GPIO et on sort de la fonction avec exit()
        exit()
except KeyboardInterrupt:
    print("CTRL-C: Terminating program.") # si le programme est utilise seul, cela permet de l'eteindre en cas d'urgence


