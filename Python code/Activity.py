import smbus                        #import SMBus module of I2C
import struct
import UpdateDB as mdb
from datetime import datetime
from time import sleep

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

Battery_bus = smbus.SMBus(1)    
Battery_Address = 0x36          # Raspi UPS HAT V1.1 address
MPU6050_bus = smbus.SMBus(3)    
MPU6050_Address = 0x68          # MPU6050 device address

def MPU_Init():
    #write to sample rate register
    MPU6050_bus.write_byte_data(MPU6050_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    MPU6050_bus.write_byte_data(MPU6050_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    MPU6050_bus.write_byte_data(MPU6050_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    MPU6050_bus.write_byte_data(MPU6050_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    MPU6050_bus.write_byte_data(MPU6050_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = MPU6050_bus.read_byte_data(MPU6050_Address, addr)
    low = MPU6050_bus.read_byte_data(MPU6050_Address, addr+1)
    #concatenate higher and lower value
    value = ((high << 8) | low)
    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value

def read_state():
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0
    #State determination
    if (Gx<-1.5 or Gy<-1.5 or Gz<-1.5 or Gx>1.5 or Gy>1.5 or Gz>1.5):
        state = 0
    elif (Ax>0.1 and Ax<0.9 and Ay>-1.2 and Ay<-0.4 and Az<0.7 and Az>-0.1):
        state = 1
    elif (Ax>0.6 and Ax<1.4 and Ay>-0.4 and Ay<0.4 and Az<0.0 and Az>-0.8):
        state = 2
    elif (Ax>0.1 and Ax<0.9 and Ay>0.4 and Ay<1.2 and Az<0.7 and Az>-0.1):
        state = 3
    elif (Ax<0.4 and Ax>-0.4 and Ay>-0.4 and Ay<0.4 and Az<1.4 and Az>0.6):
        state = 4    
    elif (Ax>-0.9 and Ax<-0.1 and Ay>-1.2 and Ay<-0.4 and Az<0.1 and Az>-0.7):
        state = 5
    elif (Ax>-1.3 and Ax<-0.5 and Ay>-0.4 and Ay<0.4 and Az<0.8 and Az>0.0):
        state = 6
    elif (Ax>-0.9 and Ax<-0.1 and Ay>0.4 and Ay<1.2 and Az<0.1 and Az>-0.7):
        state = 7
    elif (Ax<0.4 and Ax>-0.4 and Ay>-0.4 and Ay<0.4 and Az<-0.6 and Az>-1.4):
        state = 8
    else:
        state = 0
        print ("Ax=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
    #print ("The device is in position: %d" %state)
    return state

def read_voltage():
	#This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object
	read = Battery
_bus.read_word_data(Battery
_Address, 2)
	swapped = struct.unpack("<H", struct.pack(">H", read))[0]
	voltage = swapped * 78.125 /1000000
    #print "Voltage:%.2fV" % voltage
	return voltage

def read_capacity():
	#This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object
	read = Battery
_bus.read_word_data(Battery
_Address, 4)
	swapped = struct.unpack("<H", struct.pack(">H", read))[0]
	capacity = swapped/256
    #print "Battery:%i%%" % capacity
	return capacity

MPU_Init()

cur_state = 0
old_state = 0
cur_capacity = 0
old_capacity = 0

sleep(15)

while True:
    
    cur_state = read_state()
    cur_datetime = datetime.now()
    last_datetime = mdb.check_last_date()
    
    if cur_datetime.day==last_datetime.day and cur_datetime.month==last_datetime.month and cur_datetime.year==last_datetime.year:
        if old_state != cur_state:
            if old_state == 0:
                start_time = cur_datetime
                old_state = cur_state
            elif cur_state == 0:
                end_time = cur_datetime
                mdb.insert_today_activity(old_state, start_time, end_time)
                old_state = cur_state
            else:
                end_time = cur_datetime
                mdb.insert_today_activity(old_state, start_time, end_time)
                start_time = cur_datetime
                old_state = cur_state
        elif (datetime.now().hour == 23 and datetime.now().minute == 59 and datetime.now().second == 58):
            end_time = datetime.now()
            mdb.insert_today_activity(old_state, start_time, end_time)
            mdb.updates_daily_activities()
            sleep(2)
            start_time = cur_datetime 
    else:
        mdb.updates_daily_activities()
        sleep(1)
        start_time = cur_datetime
        old_state = cur_state
        
    cur_capacity = read_capacity()

    if old_capacity != cur_capacity:
        mdb.update_battery_status(read_voltage(), cur_capacity)
        old_capacity = cur_capacity
        
    sleep(1)
