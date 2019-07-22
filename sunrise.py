import RPi.GPIO as GPIO
import time

# First, turn on the relays
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, False)      # Turn on servo motor
GPIO.setup(38, GPIO.OUT)
GPIO.output(38, False)      # Turn on light bulb
GPIO.setup(15, GPIO.IN)     # Motion sensor

# Set duration of sunrise (seconds * minutes)
sunrise_duration = 60. * 15

# Set number of intervals (no. of turns)
time_interval = sunrise_duration/60.

# Set total magnitude of final brightness (as a percent)
amt_turn = 100

# Configure pin settings
GPIO.setup(03, GPIO.OUT)
pwm = GPIO.PWM(03, 50)
pwm.start(0)

# Define functions for turning servo
def WaitPeriod(waitTime):
	waitSoFar = 0
	while waitSoFar < float(waitTime):
		time.sleep(.5)
		waitSoFar += .5
		if GPIO.input(15) == 1:
			alarm_off = True
			current_time = loop_time + sunrise_duration

def TurnMotor(pct):
	duty = ((pct-100)*-1)/10. + 2
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	##time.sleep(time_interval)
	WaitPeriod(time_interval)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)

def Reset():
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(12)
	GPIO.output(03, False)
	time.sleep(2)

# Turn servo second by second
loop_time = time.time()
current_time = time.time()
secs = time_interval
alarm_off = False
while current_time < loop_time + sunrise_duration:
	TurnMotor((secs/sunrise_duration)*amt_turn)
	secs += time_interval
	current_time = time.time()
	if GPIO.input(15) == 1:
		alarm_off = True
		current_time = loop_time + sunrise_duration

# Wait for confirmation to reset
while alarm_off == False:
	if GPIO.input(15) == 0:
		pass
	else:
		alarm_off = True

# Turn off bulb relay
GPIO.output(38, True)

# Reset servo to zero
Reset()

# Turn off servo relay
GPIO.output(36, True)

# Prepare for exit
pwm.stop()
GPIO.cleanup()
