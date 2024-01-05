#-*- coding: utf-8 -*-

import time
import json

## DEVICE ID
PAJ7620_IIC_ADDR = 0x73
PAJ7620_PARTID = 0x7620

## REGISTER BANK SELECT
PAJ7620_REGITER_BANK_SEL = 0xEF

## REGISTER BANK 0
PAJ7620_ADDR_PART_ID_LOW                 = 0x00
PAJ7620_ADDR_PART_ID_HIGH                = 0x01
PAJ7620_ADDR_VERSION_ID                  = 0x01
PAJ7620_ADDR_SUSPEND_CMD                 = 0x03
PAJ7620_ADDR_GES_PS_DET_MASK_0           = 0x41
PAJ7620_ADDR_GES_PS_DET_MASK_1           = 0x42
PAJ7620_ADDR_GES_PS_DET_FLAG_0           = 0x43
PAJ7620_ADDR_GES_PS_DET_FLAG_1           = 0x44
PAJ7620_ADDR_STATE_INDICATOR             = 0x45
PAJ7620_ADDR_PS_HIGH_THRESHOLD           = 0x69
PAJ7620_ADDR_PS_LOW_THRESHOLD            = 0x6A
PAJ7620_ADDR_PS_APPROACH_STATE           = 0x6B
PAJ7620_ADDR_PS_RAW_DATA                 = 0x6C  

## REGISTER BANK 1
PAJ7620_ADDR_PS_GAIN                     = 0x44
PAJ7620_ADDR_IDLE_S1_STEP_0              = 0x67
PAJ7620_ADDR_IDLE_S1_STEP_1              = 0x68
PAJ7620_ADDR_IDLE_S2_STEP_0              = 0x69
PAJ7620_ADDR_IDLE_S2_STEP_1              = 0x6A
PAJ7620_ADDR_OP_TO_S1_STEP_0             = 0x6B
PAJ7620_ADDR_OP_TO_S1_STEP_1             = 0x6C
PAJ7620_ADDR_OP_TO_S2_STEP_0             = 0x6D
PAJ7620_ADDR_OP_TO_S2_STEP_1             = 0x6E
PAJ7620_ADDR_OPERATION_ENABLE            = 0x72

PAJ7620_BANK0                            = 0
PAJ7620_BANK1                            = 1

## PAJ7620_ADDR_SUSPEND_CMD
PAJ7620_I2C_WAKEUP                       = 0x01
PAJ7620_I2C_SUSPEND                      = 0x00

## PAJ7620_ADDR_OPERATION_ENABLE
PAJ7620_ENABLE                           = 0x01
PAJ7620_DISABLE                          = 0x00

## You can adjust the reaction time according to the actual circumstance.
GES_REACTION_TIME                        = 0.05 
## When you want to recognize the Forward/Backward gestures, your gestures' reaction time must less than GES_ENTRY_TIME(0.8s).
GES_ENTRY_TIME                           = 2
GES_QUIT_TIME                            = 1

GESTURE = json.loads('{\
 "0": "None",\
 "1": "Right",\
 "2": "Left",\
 "4": "Up",\
 "8": "Down",\
 "16": "Forward",\
 "32": "Backward",\
 "64":"Clockwise",\
 "128": "Anti-Clockwise",\
 "256":"Wave",\
 "512":"WaveSlowlyDisorder",\
 "3": "WaveSlowlyLeftRight",\
 "12": "WaveSlowlyUpDown",\
 "48": "WaveSlowlyForwardBackward"}')

class PAJ7620U2:
   ## OK
   ERR_OK = 0
   ## Error in Data Bus
   ERR_DATA_BUS = -1
   ## IC version mismatch
   ERR_IC_VERSION = -2
   ## no gestures detected
   GESTURE_NONE  = 0x00
   ## move from left to right
   GESTURE_RIGHT = 0x01 << 0
   ## move from right to left
   GESTURE_LEFT = 0x01 << 1
   ## move from down to up
   GESTURE_UP = 0x01 << 2
   ## move form up to down
   GESTURE_DOWN = 0x01 << 3
   ## starts far, move close to sensor
   GESTURE_FORWARD = 0x01 << 4
   ## starts near, move far to sensor
   GESTURE_BACKWARD = 0x01 << 5
   ## clockwise
   GESTURE_CLOCKWISE = 0x01 << 6
   ## anti - clockwise
   GESTURE_ANTI_CLOCKWISE = 0x01 << 7
   ## wave quickly
   GESTURE_WAVE = 0x01 << 8
   ##wave randomly and slowly
   GESTURE_WAVE_SLOWLY_DISORDER = 0x01 << 9
   ## slowly move left and right
   GESTURE_WAVE_SLOWLY_LEFT_RIGHT = GESTURE_LEFT + GESTURE_RIGHT
   ## slowly move up and down
   GESTURE_WAVE_SLOWLY_UP_DOWN = GESTURE_UP + GESTURE_DOWN
   ##slowly move forward and backward
   GESTURE_WAVE_SLOWLY_FORWARD_BACKWARD = GESTURE_FORWARD + GESTURE_BACKWARD
   ## support all gestures, no practical meaning, only suitable for writing abstract program logic.
   GESTURE_ALL = 0xff
   ## some registers are located in Bank0
   BANK_0 = 0
   ## some registers are located in Bank1
   BANK_1 = 1
   ## Gesture Update Rate is 120HZ, Gesture speed is 60°/s - 600°/s
   NORMAL_RATE = 0
   ## Gesture Update Rate is 240HZ,Gesture speed is 60°/s - 1200°/s
   GAMING_RATE = 1

   _gesture_highrate = True

   _init_register_array = [
      [0xEF,0x00],
      [0x32,0x29],
      [0x33,0x01],
      [0x34,0x00],
      [0x35,0x01],
      [0x36,0x00],
      [0x37,0x07],
      [0x38,0x17],
      [0x39,0x06],
      [0x3A,0x12],
      [0x3F,0x00],
      [0x40,0x02],
      [0x41,0xFF],
      [0x42,0x01],
      [0x46,0x2D],
      [0x47,0x0F],
      [0x48,0x3C],
      [0x49,0x00],
      [0x4A,0x1E],
      [0x4B,0x00],
      [0x4C,0x20],
      [0x4D,0x00],
      [0x4E,0x1A],
      [0x4F,0x14],
      [0x50,0x00],
      [0x51,0x10],
      [0x52,0x00],
      [0x5C,0x02],
      [0x5D,0x00],
      [0x5E,0x10],
      [0x5F,0x3F],
      [0x60,0x27],
      [0x61,0x28],
      [0x62,0x00],
      [0x63,0x03],
      [0x64,0xF7],
      [0x65,0x03],
      [0x66,0xD9],
      [0x67,0x03],
      [0x68,0x01],
      [0x69,0xC8],
      [0x6A,0x40],
      [0x6D,0x04],
      [0x6E,0x00],
      [0x6F,0x00],
      [0x70,0x80],
      [0x71,0x00],
      [0x72,0x00],
      [0x73,0x00],
      [0x74,0xF0],
      [0x75,0x00],
      [0x80,0x42],
      [0x81,0x44],
      [0x82,0x04],
      [0x83,0x20],
      [0x84,0x20],
      [0x85,0x00],
      [0x86,0x10],
      [0x87,0x00],
      [0x88,0x05],
      [0x89,0x18],
      [0x8A,0x10],
      [0x8B,0x01],
      [0x8C,0x37],
      [0x8D,0x00],
      [0x8E,0xF0],
      [0x8F,0x81],
      [0x90,0x06],
      [0x91,0x06],
      [0x92,0x1E],
      [0x93,0x0D],
      [0x94,0x0A],
      [0x95,0x0A],
      [0x96,0x0C],
      [0x97,0x05],
      [0x98,0x0A],
      [0x99,0x41],
      [0x9A,0x14],
      [0x9B,0x0A],
      [0x9C,0x3F],
      [0x9D,0x33],
      [0x9E,0xAE],
      [0x9F,0xF9],
      [0xA0,0x48],
      [0xA1,0x13],
      [0xA2,0x10],
      [0xA3,0x08],
      [0xA4,0x30],
      [0xA5,0x19],
      [0xA6,0x10],
      [0xA7,0x08],
      [0xA8,0x24],
      [0xA9,0x04],
      [0xAA,0x1E],
      [0xAB,0x1E],
      [0xCC,0x19],
      [0xCD,0x0B],
      [0xCE,0x13],
      [0xCF,0x64],
      [0xD0,0x21],
      [0xD1,0x0F],
      [0xD2,0x88],
      [0xE0,0x01],
      [0xE1,0x04],
      [0xE2,0x41],
      [0xE3,0xD6],
      [0xE4,0x00],
      [0xE5,0x0C],
      [0xE6,0x0A],
      [0xE7,0x00],
      [0xE8,0x00],
      [0xE9,0x00],
      [0xEE,0x07],
      [0xEF,0x01],
      [0x00,0x1E],
      [0x01,0x1E],
      [0x02,0x0F],
      [0x03,0x10],
      [0x04,0x02],
      [0x05,0x00],
      [0x06,0xB0],
      [0x07,0x04],
      [0x08,0x0D],
      [0x09,0x0E],
      [0x0A,0x9C],
      [0x0B,0x04],
      [0x0C,0x05],
      [0x0D,0x0F],
      [0x0E,0x02],
      [0x0F,0x12],
      [0x10,0x02],
      [0x11,0x02],
      [0x12,0x00],
      [0x13,0x01],
      [0x14,0x05],
      [0x15,0x07],
      [0x16,0x05],
      [0x17,0x07],
      [0x18,0x01],
      [0x19,0x04],
      [0x1A,0x05],
      [0x1B,0x0C],
      [0x1C,0x2A],
      [0x1D,0x01],
      [0x1E,0x00],
      [0x21,0x00],
      [0x22,0x00],
      [0x23,0x00],
      [0x25,0x01],
      [0x26,0x00],
      [0x27,0x39],
      [0x28,0x7F],
      [0x29,0x08],
      [0x30,0x03],
      [0x31,0x00],
      [0x32,0x1A],
      [0x33,0x1A],
      [0x34,0x07],
      [0x35,0x07],
      [0x36,0x01],
      [0x37,0xFF],
      [0x38,0x36],
      [0x39,0x07],
      [0x3A,0x00],
      [0x3E,0xFF],
      [0x3F,0x00],
      [0x40,0x77],
      [0x41,0x40],
      [0x42,0x00],
      [0x43,0x30],
      [0x44,0xA0],
      [0x45,0x5C],
      [0x46,0x00],
      [0x47,0x00],
      [0x48,0x58],
      [0x4A,0x1E],
      [0x4B,0x1E],
      [0x4C,0x00],
      [0x4D,0x00],
      [0x4E,0xA0],
      [0x4F,0x80],
      [0x50,0x00],
      [0x51,0x00],
      [0x52,0x00],
      [0x53,0x00],
      [0x54,0x00],
      [0x57,0x80],
      [0x59,0x10],
      [0x5A,0x08],
      [0x5B,0x94],
      [0x5C,0xE8],
      [0x5D,0x08],
      [0x5E,0x3D],
      [0x5F,0x99],
      [0x60,0x45],
      [0x61,0x40],
      [0x63,0x2D],
      [0x64,0x02],
      [0x65,0x96],
      [0x66,0x00],
      [0x67,0x97],
      [0x68,0x01],
      [0x69,0xCD],
      [0x6A,0x01],
      [0x6B,0xB0],
      [0x6C,0x04],
      [0x6D,0x2C],
      [0x6E,0x01],
      [0x6F,0x32],
      [0x71,0x00],
      [0x72,0x01],
      [0x73,0x35],
      [0x74,0x00],
      [0x75,0x33],
      [0x76,0x31],
      [0x77,0x01],
      [0x7C,0x84],
      [0x7D,0x03],
      [0x7E,0x01]]

   def __init__(self, bus):
       '''!
         @brief Constuctor
         @param bus  iic bus
       '''
       self.i2c_addr = PAJ7620_IIC_ADDR
       self.i2cbus = bus
       self._gesture_high_rate = True

   def begin(self):
      '''!
         @brief init function
         @return return 0 if initialization succeeds, otherwise return non-zero. 
      '''
      self._select_bank(self.BANK_0)
      partid = self._read_reg(PAJ7620_ADDR_PART_ID_LOW, 4)
      if partid == None:
      #   print("bus data access error")
        return self.ERR_DATA_BUS
      time.sleep(0.1)
      if (partid[1]<<8|partid[0]) != PAJ7620_PARTID:
        return self.ERR_IC_VERSION
      for i in range(0,len(self._init_register_array)):
        self._write_reg(self._init_register_array[i][0], [self._init_register_array[i][1]])
      self._select_bank(self.BANK_0)
      return self.ERR_OK

   def set_gesture_highrate(self,v):
      '''!
        @brief Set gesture detection mode 
        @param v true Set to fast detection mode, recognize gestures quickly and return. 
        @n  false Set to slow detection mode, system will do more judgements. 
        @n  In fast detection mode, the sensor can recognize 9 gestures: move left, right, up, down,
        @n  forward, backward, clockwise, counter-clockwise, wave. 
        @n  To detect the combination of these gestures, like wave left, right and left quickly, users need to design their own 
        @n  algorithms logic.
        @n  Since users only use limited gestures, we didn't integrate too much expanded gestures in the library. 
        @n  If necessary, you can complete the algorithm logic in the ino file by yourself.
        @n
        @n
        @n  In slow detection mode, the sensor recognize one gesture every 2 seconds, and we have integrated the expanded gestures 
        @n  inside the library, which is convenient for the beginners to use.
        @n  The slow mode can recognize 9  basic gestures and 4 expanded gestures: move left, right, up, down, forward, backward, 
        @n  clockwise, counter-clockwise, wave, slowly move left and right, slowly move up and down, slowly move forward and backward, 
        @n  wave slowly and randomly. 
      '''
      self._gesture_highrate = v

   def gesture_description(self,gesture):
      '''!
        @brief Get the string descritpion corresponding to the gesture number.
        @param gesture Gesture number inlcuded in the eGesture_t
        @return Textual description corresponding to the gesture number:if the gesture input in the gesture table doesn't exist,
        @n return null string.
      '''
      ges = str(gesture)
      return GESTURE.get(ges, "")
   
   def get_gesture(self):
      '''!
        @brief Get gesture
        @return Return gesture, could be any value except GESTURE_ALL in eGesture_t.
      '''
      buf = self._read_reg(PAJ7620_ADDR_GES_PS_DET_FLAG_1, 4)
      gesture = buf[0] << 8
      if gesture == self.GESTURE_WAVE:
         # print("Wave1 Event Detected")
         time.sleep(GES_QUIT_TIME)
      else :
         gesture = self.GESTURE_NONE
         buf = self._read_reg(PAJ7620_ADDR_GES_PS_DET_FLAG_0, 4) # Read BANK_0_Reg_0x43 / 0x44 for gesture result.
         gesture = buf[0] & 0x00ff
         if not self._gesture_highrate:
            time.sleep(GES_ENTRY_TIME)
            tmp = self._read_reg(PAJ7620_ADDR_GES_PS_DET_FLAG_0, 4)
            #print(tmp)
            #print("tmp=%#x"%tmp[0])
            #print("gesture=%#x" % gesture)
            time.sleep(0.2)
            gesture = gesture|tmp[0]
         if gesture != self.GESTURE_NONE:
            #print("")
            time.sleep(0.1)
         elif gesture == self.GESTURE_RIGHT:
            pass        #print("Right Event Detected")
         elif gesture == self.GESTURE_LEFT:
            pass        #print("Left Event Detected")
         elif gesture== self.GESTURE_UP:
            pass        #print("Up Event Detected")
         elif gesture== self.GESTURE_DOWN:
            pass        #print("Down Event Detected")
         elif gesture == self.GESTURE_FORWARD:
            #print("Forward Event Detected")
            if not self._gesture_highrate:
               time.sleep(GES_QUIT_TIME)
            else:
               time.sleep(GES_QUIT_TIME / 5)
         elif gesture == self.GESTURE_BACKWARD:
            #print("Backward Event Detected")
            if not self._gesture_high_rate:
               time.sleep(GES_QUIT_TIME)
            else:
               time.sleep(GES_QUIT_TIME / 5)
         elif gesture == self.GESTURE_CLOCKWISE:
            pass        #print("Clockwise Event Detected")
         elif gesture == self.GESTURE_ANTI_CLOCKWISE:
            pass        #print("anti-clockwise Event Detected")
         else:
            tmp = self._read_reg(PAJ7620_ADDR_GES_PS_DET_FLAG_1, 4)
            if tmp[0]:
               gesture = self.GESTURE_WAVE
               #print("Wave2 Event Detected")
            else:
               if gesture == self.GESTURE_WAVE_SLOWLY_LEFT_RIGHT:
                  pass        #print("LeftRight Wave Event Detected")
               elif gesture == self.GESTURE_WAVE_SLOWLY_UP_DOWN:
                  pass        #print("UpDown Wave Event Detected")
               elif gesture == self.GESTURE_WAVE_SLOWLY_FORWARD_BACKWARD:
                  pass        #print("ForwardBackward Wave Event Detected")
               elif gesture == self.GESTURE_WAVE_SLOWLY_DISORDER:
                  pass        #print("Wave Disorder Event Detected")
      return gesture

   def _select_bank(self,data):
      '''!
        @brief Switch Bank
        @param bank  The bank you will switch to, BANK_0 or BANK_1
        @return Return 0 if switching successfully, otherwise return non-zero. 
      '''
      if data == self.BANK_0 or data == self.BANK_1:
         self._write_reg(PAJ7620_REGITER_BANK_SEL, [data])

   def _set_normal_or_gaming_mode(self, mode):
      '''!
        @brief Set rate mode of the module, the API is disabled currently.
        @param mode The mode users can configure, NORMAL_RATE or GAMING_RATE
        @return Return 0 if setting is successful, otherwise return non-zero. 
      '''
      if mode == self.NORMAL_RATE or mode == self.GAMING_RATE:
         return 0

   def _write_reg(self,reg,value):
      '''!
        @brief Write register function 
        @param reg  register address 8bits
        @param pBuf Storage cache of the data to be written into 
        @param size Length of the data to be written into 
      '''
      self.i2cbus.writeto_mem(self.i2c_addr, reg, bytes(value))

   def _read_reg(self, reg, len):
      '''!
        @brief Read register function 
        @param reg  register address 8bits
        @param pBuf Storage cache of the data to be read
        @param size Length of the data to be read
        @return Return the actually read length, fails to read if return 0.
      '''
      try:
         return self.i2cbus.readfrom_mem(self.i2c_addr, reg, len)
      except:
         return b'\x00\x00\x00\x00'

   def scan(self):
      '''!
        @brief Check whether the sensor is connected to the bus
        @return Return the actually read length, fails to read if return 0.
      '''
      try:
        return self.i2c_addr in self.i2cbus.scan()
      except:
        print("I2C init fail")
        return False