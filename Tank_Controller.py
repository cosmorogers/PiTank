from Adafruit_PWM_Servo_Driver import PWM
import time
import RPi.GPIO as io
import time

class TankController:
  
  right_en = 0
  right_a  = 1
  right_b  = 2
  left_en  = 4
  left_a   = 5
  left_b   = 6
  turt_en  = 8
  turt_a   = 9
  turt_b   = 10
  
  pwm      = PWM(0x40, debug=False)
  pwmMax   = 4095
  pwmMin   = 2500
  pwmDiff  = 1595
  
  def __init(self):
    io.setmode(io.BOARD)
    pwm.setPWMFreq(60)
    
  def left_clockwise(self):
    self.pwm.setPWM(self.left_a, 0, self.pwmMax)
    self.pwm.setPWM(self.left_b, 0, 0)    
    
  def left_counter_clockwise(self):
    self.pwm.setPWM(self.left_a, 0, 0)
    self.pwm.setPWM(self.left_b, 0, self.pwmMax)
    
    
  def right_clockwise(self):
    self.pwm.setPWM(self.right_a, 0, self.pwmMax)
    self.pwm.setPWM(self.right_b, 0, 0)
    
  def right_counter_clockwise(self):
    self.pwm.setPWM(self.right_a, 0, 0)
    self.pwm.setPWM(self.right_b, 0, self.pwmMax)
    
  def drive(self, left_speed, right_speed):
    print 'left speed %s' %left_speed
    print 'right speed %s' % right_speed
      
    if -1 <= left_speed <= 1 and -1 <= right_speed <= 1:
      if left_speed > 0:
        self.left_clockwise()
      else:
        self.left_counter_clockwise()
        
      if right_speed > 0:
        self.right_clockwise()
      else:
        self.right_counter_clockwise()
        
      if left_speed != 0 :
        left_speed = int(self.pwmMin + (self.pwmDiff * abs(left_speed)))
        
      if right_speed !=0 :
        right_speed = int(self.pwmMin + (self.pwmDiff * abs(right_speed)))
      
      if left_speed < self.pwmMin:
        left_speed = 0
        
      if right_speed < self.pwmMin:
        right_speed = 0
      
      print 'left speed %s' %left_speed
      print 'right speed %s' % right_speed
      
      self.pwm.setPWM(self.left_en, 0, left_speed)
      self.pwm.setPWM(self.right_en, 0, right_speed)
    
    else:
      #error
      print "Speed too big"
      
  def got_message(self, message):
    commands = { 
      'forward': self.forward, 
      'stop': self.stop,
      'backwards': self.backwards,
      'left-forward': self.left_forward,
      'right-forward': self.right_forward,
      'rotate-left': self.rotate_left,
      'rotate-right': self.rotate_right,
      'left-backwards': self.left_backwards,
      'right-backwards': self.right_backwards,
      'turret-left': self.turret_left,
      'turret-right': self.turret_right
    }
    msg = message.split(',')
    command = msg[0]
    speed = float(msg[1])
    print command
    print 'Got command %s' % command
    print 'Speed %s' % speed
    
    commands[command](speed)
    
  def forward(self, speed):
    self.drive(speed/100, speed/100)
    
  def stop(self, speed):
    self.drive(0,0)
    
  def backwards(self, speed):
    self.drive(speed/-100, speed/-100)
    
  def left_forward(self, speed):
    self.drive(0, speed/100)
    
  def right_forward(self, speed):
    self.drive(speed/100, 0)
    
  def rotate_left(self, speed):
    self.drive(speed/-100, speed/100)
    
  def rotate_right(self, speed):
    self.drive(speed/100, speed/-100)
    
  def left_backwards(self, speed):
    self.drive(0, speed/-100)
    
  def right_backwards(self, speed):
    self.drive(speed/-100, 0)
    
  def turret_left(self, speed):
    self.pwm.setPWM(self.turt_a, 0, self.pwmMax)
    self.pwm.setPWM(self.turt_b, 0, 0)
    self.pwm.setPWM(self.turt_en, 0, (self.pwmMin + (self.pwmDiff/2)) )
    
    time.sleep(0.5)
    self.pwm.setPWM(self.turt_en, 0, 0)
    
    
  def turret_right(self, speed):
    self.pwm.setPWM(self.turt_a, 0, 0)
    self.pwm.setPWM(self.turt_b, 0, self.pwmMax)   
    self.pwm.setPWM(self.turt_en, 0, (self.pwmMin + (self.pwmDiff/2)) )   
    
    time.sleep(0.5)
    self.pwm.setPWM(self.turt_en, 0, 0)
    
    
   
