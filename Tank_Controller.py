from Adafruit_PWM_Servo_Driver import PWM
import time
import RPi.GPIO as io


class TankController:
  
  right_en = 0
  right_a  = 1
  right_b  = 2
  left_en  = 4
  left_a   = 5
  left_b   = 6
  
  pwm      = PWM(0x40, debug=False)
  pwmMax   = 4095
  pwmMin   = 2500
  pwmDiff  = 1595
  
  def __init(self):
    io.setmode(io.BOARD)
    pwm.setPWMFreq(60)
    
  def left_clockwise():
    pwm.setPWM(left_a, 0, 0)
    pwm.setPWM(left_b, 0, pwmMax)
    
  def left_counter_clockwise():
    pwm.setPWM(left_a, 0, pwmMax)
    pwm.setPWM(left_b, 0, 0)    
    
  def right_clockwise():
    pwm.setPWM(right_a, 0, 0)
    pwm.setPWM(right_b, 0, pwmMax)
    
  def right_counter_clockwise():
    pwm.setPWM(right_a, 0, pwmMax)
    pwm.setPWM(right_b, 0, 0)
    
  def drive(left_speed, right_speed):
    
    if -1 <= left_speed <= 1 and -1 <= right_speed <= 1:
      if left_speed > 0:
        left_clockwise()
      else:
        left_counter_clockwise()
        
      if right_speed > 0:
        right_clockwise()
      else:
        right_counter_clockwise()
        
      
      left_speed = pwmDiff * abs(left_speed)
      right_speed = pwmDiff * abs(right_speed)
      
      pwm.setPWM(left_en, 0, left_speed)
      pwm.setPWM(right_en, 0, right_speed)
    
    else:
      #error
      print "Speed too big"
    
    
