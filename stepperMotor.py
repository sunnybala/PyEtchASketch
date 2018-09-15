import RPi.GPIO as GPIO
import time

class stepperMotor(object):
    def __init__(self, control_pins):
        GPIO.setmode(GPIO.BOARD)
        self.control_pins = control_pins
        self.halfstep_seq = [
                      [1,0,0,0],
                      [1,1,0,0],
                      [0,1,0,0],
                      [0,1,1,0],
                      [0,0,1,0],
                      [0,0,1,1],
                      [0,0,0,1],
                      [1,0,0,1]
                    ]
        self.prev = 0
    
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
            
    def rotate(self,n):
        n = int(n)
        if n < 0:
            ii = -1
        elif n > 0:
            ii = 1
        else:
            return
        if ii != self.prev:
            print('re-aligning')
            n += 24*ii
        for i in range(int(abs(n))):
          for halfstep in range(8):
            for pin in range(4):
              GPIO.output(self.control_pins[pin], self.halfstep_seq[::ii][halfstep][pin])
            time.sleep(0.002)
        self.prev = ii
        
    def close(self):
        GPIO.cleanup()



