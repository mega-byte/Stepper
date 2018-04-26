# stepper.py   20-Dec-17

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) 

#enable_pin = nn
coil_A_1_pin = 15 # pink 
coil_A_2_pin = 18 # orange
coil_B_1_pin = 19 # blue
coil_B_2_pin = 22 # yellow

# GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# GPIO.output(enable_pin, 1)

def forward(delay, steps):
  print 'STEPPER: Now in the stepper program'  
  for i in range(0, steps):
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 0)
    time.sleep(delay)
    setStep(1, 1, 0, 0)
    time.sleep(delay)
    setStep(1, 0, 0, 0)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 0, 1, 1)
    time.sleep(delay)
    setStep(0, 0, 1, 0)
    time.sleep(delay)
  setStep(0, 0, 0, 0)

def backwards(delay, steps):
  print 'STEPPER: Now in stepper'  
  for i in range(0, steps):
    setStep(0, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 0, 1, 1)
    time.sleep(delay)
    setStep(0, 0, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 0)
    time.sleep(delay)
    setStep(1, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
  setStep(0, 0, 0, 0)

def blink(delay,steps):
  print 'STEPPER: The stepper motor LEDs will now blink...'
  for i in range(0, steps):
    setStep(1, 1, 1, 1)
    time.sleep(delay)
    setStep(0, 0, 0, 0)
    time.sleep(delay)
 
def cleanup():
  print
  print 'STEPPER: Program exiting cleanly....'
  GPIO.cleanup()
  
def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

# The section below can be used if using this module stand alone..
if __name__ == '__main__':
  print 'Stepper.py is running stand alone.....type ^C to exit'
  try:
    while True:
      delay = raw_input("Delay between steps (milliseconds)?")
      steps = raw_input("How many steps forward? ")
      forward(int(delay) / 1000.0, int(steps))
      steps = raw_input("How many steps backwards? ")
      backwards(int(delay) / 1000.0, int(steps))
      blink(0.020,50)
  except:
    cleanup()
  
