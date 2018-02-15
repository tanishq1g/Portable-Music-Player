from mpu6050 import mpu6050
import time
import math

sensor = mpu6050(0x68)
t = 1
octaves = [[16.3,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96,27.50,29.14,30.87],[32.70,34.65,36.71,38.89,41.20,43.65,46.25,49.00,51.91,55.00,58.27,61.74],[65.41,69.30,73.42,77.78,82.41,87.31,92.50,98.00,103.8,110.0,116.5,123.5],[130.8,138.6,146.8,155.6,164.8,174.6,185.0,196.0,207.7,220.0,233.1,246.9],[261.6,277.2,293.7,311.1,329.6,349.2,370.0,392.0,415.3,440.0,466.2,493.9],[523.3,554.4,587.3,622.3,659.3,698.5,740.0,784.0,830.6,880.0,932.3,987.8],[1047,1109,1175,1245,1319,1397,1480,1568,1661,1760,1865,1976],[2093,2217,2349,2489,2637,2794,2960,3136,3322,3520,3729,3951],[4186,4435,4699,4978,5274,5588,5920,6272,6645,7040,7459,7902]]
def orientation_acc(x,y,z):
	y -= math.pi/2
	z -= math.pi/2
	per_tilt_x = (x * 180 / math.pi)*0.9
	per_tilt_y = (y * 180 / math.pi)*0.9
	per_tilt_z = (z * 180 / math.pi)*0.9

	# print x,y,z
	print -1 * per_tilt_y , "percent tilt for volume movement"
	# print per_tilt_x , per_tilt_y , per_tilt_z

	if (-1*per_tilt_y) < 2.9:
		x -= math.pi
		per_tilt_x = (x * 180 / math.pi)*0.9
		if per_tilt_z < 0:
			print " octave movement : " , -1 * per_tilt_x
		else:
			print " octave movement : " , per_tilt_x

while t == 1:
	print "\n"
	time.sleep(1.5)
	data = sensor.get_accel_data()
	# print "acc  : " , sensor.get_accel_data()
	r_acc = pow((pow(data["x"],2) + pow(data["y"],2) + pow(data["z"],2)),0.5)
	x_angle = math.acos(data["x"]/r_acc)
	y_angle = math.acos(data["y"]/r_acc)
	z_angle = math.acos(data["z"]/r_acc)
	# print r_acc , "    x : ", x_angle ,"y : ",  y_angle ,"z : ",  z_angle
	orientation_acc(x_angle,y_angle,z_angle)


	# print "gyro : " , sensor.get_gyro_data()
	# data2 = sensor.get_gyro_data()
	# r_gyro = pow((pow(data2["x"],2) + pow(data2["y"],2) + pow(data2["z"],2)),0.5)
	# x_angle = math.acos(data2["x"]/r_gyro)
	# y_angle = math.acos(data2["y"]/r_gyro)
	# z_angle = math.acos(data2["z"]/r_gyro)
	# print r_gyro , "x : ", x_angle ,"y : ",  y_angle ,"z : ",  z_angle
	# t = input("wish to proceed")
