import numpy as np
import serial
from serial.tools import list_ports
import time

class NewportESPMotionController(object):

#initialize and connect
	def __init__(self,port="COM9", timeout=5, debug=True):
		self.port = port
		self.debug = debug
		self.baudrate = 921600
		self.ser = serial.Serial(port=port,baudrate=self.baudrate,timeout=timeout)

	def disconnect(self):
		self.ser.close()

	def connect(self):
		self.ser.open()

# Send Commands, Recieve data, Iterate over multiple axes ---------------------

	def SendString(self,stringIn):
		# Sends string to serial port, appends line feed + carriage return
		stringOut = stringIn+'\n\r'
		self.ser.write(stringOut)
#		print(stringOut)

	def ReadString(self):
		# Reads line from serial port,
		output = self.ser.readline()
		return(output)

	def ReadData(self,datatype=float): 
		# Read line from serial port, converts to specified datatype
		strOut = self.ser.readline()
		output = datatype(strOut)
		return(output)

	def SendCommand(self,axis,code,value="   ",read=False,datatype=float):
		# Generates and sends command with format: Axis + two letter Command Code + Parameter Value
		# Accepts axis as a single number, tuple, or lists of length 1,2, or 3
		response=0
		if type(axis)==int:
			strOut = str(axis) + code + str(value)
			self.SendString(strOut)
			if read:
				response = self.ReadData(datatype=datatype)
			return(response)
		if axis=='all' or axis=='ALL':
			axis = (1,2,3)
		if type(axis)==list or tuple:
			response = []
			for i in range(len(axis)):
				strOut = str(axis[i]) + code + str(value[i])
				self.SendString(strOut)
				if read:
					response.append(self.ReadData(datatype=datatype))
			return(tuple(response))


# Motor Enable and Status ----------------------------------------------------

	def enable(self,axis,datatype=bool):
		self.SendCommand(axis,"MO")
		response = self.SendCommand(axis,"MO?",read=True,datatype=datatype)
		return(response)

	def	disable(self,axis,datatype=bool):
		self.SendCommand(axis,"MF")
		response = self.SendCommand(axis,"MF?",read=True,datatype=datatype)
		return(response)

	def status_MotorEnabled(self,axis,datatype=bool):
		response = self.SendCommand(axis,"MO?",read=True,datatype=datatype)
		return(response)

# Motion Control --------------------------------------------------           

	def move(self, axis,position,wait=False):
		# PA Move absolute ♦ ♦ ♦ 3- 106
		if position>=0:
			stringOut = '%dPA+%0.5f' %(axis,position)
		if position<0:
			stringOut = '%dPA-%0.5f' %(axis,position)
		if wait==True:
			stringOut = stringOut + ';%dWS' %axis
		self.SendString(stringOut)

	def jog(self,axis,delta):
		# PR Move relative ♦ ♦ ♦ 3- 110
		strOut = "%dPR%0.5f" %(axis,delta)
		SendString(strOut)

	def abort(self): # Stop all motion and disable all motors
		SendString('AB')

	def stop(self): #stop motion
		SendString('ST')

	def set_PositionOffset(self,axis,):
		selfSH

	def home():
		# set home position
		pass

	def set_home(self,axis,position):
		self.SendCommand(axis,'SH',position) 
	# command defines the value that is loaded in the position counter when home
	# is found. The default value for all motion devices is 0. This means that unless a
	# new value is defined using this command, the home position will be set to 0
	# when a home search is initiated using the OR command or from the front panel 

# Position Requests ----------------------------------------------------------

	def get_Position(self,axis=1): # Get true position, accepts integer or tuple for desired axis
		response = self.SendCommand(axis=axis,code="TP?")
		return(response)

	def get_Destination(self,axis=1): # Get desired/goal position, accepts integer or tuple for desired axis
		response = self.SendCommand(axis=axis,code="DP?")
		return(response)


# TESTING Stuff below --------------------------------------------------------

if True: 
	ESP301 = NewportESPMotionController("COM9"); print('connected')

	ESP301.enable("all")

	ESP301.disconnect(); print('disconnected')



if False: # Test move and read position functions
	ESP301 = NewportESPMotionController("COM9"); print('connected')
	mv = ESP301.move(1,0.12345)
	mv = ESP301.move(2,0.01234)
	mv = ESP301.move(3,0.00123)
	print('move requested')

	time.sleep(0.1)

	print("read positions")
	a = np.zeros((3,3))
	a[0,0] = ESP301.get_Position(1)
	a[1,0] = ESP301.get_Position(2)
	a[2,0] = ESP301.get_Position(3)

	print("read Destinations")
	a[0,1] = ESP301.get_Destination(1)
	a[1,1] = ESP301.get_Destination(2)
	a[2,1] = ESP301.get_Destination(3)

	time.sleep(5)

	print("read positions again")
	b = ESP301.get_Position([1,2,3])
	ESP301.disconnect(); print('disconnected')


'''
GENERAL MODE SELECTION
BQ Enable/disable DIO jog mode ♦ ♦ ♦ 3- 39
DO Set DAC offset ♦ ♦ ♦ 3- 51
FP Set position display resolution ♦ ♦ ♦ 3- 58
LC Lock/Unlock keyboard ♦ ♦ 3- 92
MF Power OFF ♦ ♦ ♦ 3- 95
MO Power ON ♦ ♦ ♦ 3- 96
QD Update Unidriver amplifier ♦ ♦ ♦ 3- 111
RS Reset the controller ♦ ♦ 3- 121
TJ Set trajectory mode ♦ ♦ 3- 137
ZA Set amplifier configuration ♦ ♦ 3- 155
ZB Set feedback configuration ♦ ♦ 3- 158
ZE Set E-stop configuration ♦ ♦ 3- 160
ZF Set following error configuration ♦ ♦ 3- 162
ZH Set hardware limit configuration ♦ ♦ 3- 164
ZS Set software limit configuration ♦ ♦ 3- 166
ZU Get ESP system configuration ♦ ♦ 3- 168
ZZ Set system configuration ♦ ♦ 3- 170

STATUS FUNCTIONS
DP Get target position ♦ ♦ 3- 52
DV Get working speed ♦ ♦ 3- 53
ID Get stage model and serial number ♦ ♦ 3- 83
MD Get axis motion status ♦ ♦ 3- 94
PH Get hardware status ♦ ♦ 3- 107
TB Get error message ♦ ♦ 3- 135
TE Get error number ♦ ♦ 3- 136
TP Get position ♦ ♦ 3- 138
TS Get controller status ♦ ♦ 3- 139
TV Get velocity ♦ ♦ 3- 140
TX Get controller activity ♦ ♦ 3- 141
VE Get firmware version ♦ ♦ 3- 147
XM Get available program memory ♦ ♦ 3- 153

MOTION & POSITION CONTROL
AB Abort motion ♦ ♦ 3- 21
DH Define home ♦ ♦ 3- 49
MT Move to hardware travel limit ♦ ♦ ♦ 3- 97
MV Move indefinitely ♦ ♦ ♦ 3- 98
MZ Move to nearest index ♦ ♦ 3- 100
OR Origin searching ♦ ♦ ♦ 3- 104
PA Move absolute ♦ ♦ ♦ 3- 106
PR Move relative ♦ ♦ ♦ 3- 110
ST Stop motion ♦ ♦ ♦ 3- 133

MOTION DEVICE PARAMETERS
FE Set following error threshold ♦ ♦ ♦ 3- 57
FR Full step resolution ♦ ♦ ♦ 3- 59
GR Set gear ratio ♦ ♦ ♦ 3- 60
QG Set gear constant ♦ ♦ 3- 112
QI Motor current ♦ ♦ 3- 113
QM Define motor type ♦ ♦ 3- 114
QR Torque reduction ♦ ♦ ♦ 3- 116
QS Set microstep factor ♦ ♦ 3- 117
QT Define tachometer constant ♦ ♦ 3- 118
QV Set motor voltage ♦ ♦ 3- 119
SI Set master-slave jog update interval ♦ ♦ ♦ 3- 126
SK Set slave axis jog velocity
coefficients
♦ ♦ ♦ 3- 127
SL Set left limit ♦ ♦ ♦ 3- 128
SN Set units ♦ ♦ 3- 130
SR Set right limit ♦ ♦ 3- 131
SS Set master-slave relationship ♦ ♦ 3- 132
SU Set encoder resolution ♦ ♦ 3- 134

PROGRAMMING
DL Define label ♦ 3- 50
EO Automatic execution on power on ♦ ♦ 3- 54
EP Enter program download mode ♦ 3- 55
EX Execute stored program ♦ ♦ 3- 56
JL Jump to label ♦ ♦ 3- 86
LP List program ♦ ♦ 3- 92
QP Quit program mode ♦ 3- 115
SM Save to non-volatile memory ♦ 3- 129
XM Get available program memory ♦ ♦ 3- 153
XX Delete a stored program ♦ ♦ 3- 154

TRAJECTORY DEFINITION
AC Set acceleration ♦ ♦ ♦ 3- 22
AE Set e-stop deceleration ♦ ♦ ♦ 3- 24
AG Set deceleration ♦ ♦ ♦ 3- 27
AU Set maximum acceleration ♦ ♦ ♦ 3- 30
BA Set backlash compensation ♦ ♦ ♦ 3- 31
CO Set linear compensation ♦ ♦ ♦ 3- 41
JH Set jog high speed ♦ ♦ ♦ 3- 84
JK Set jerk rate ♦ ♦ ♦ 3- 85
JW Set jog low speed ♦ ♦ ♦ 3- 87
OL Set home search low speed ♦ ♦ ♦ 3- 102
OH Set home search high speed ♦ ♦ ♦ 3- 101
OM Set home search mode ♦ ♦ ♦ 3- 103
SH Set home preset position ♦ ♦ ♦ 3- 125
UF Update filter parameters ♦ ♦ ♦ 3- 142
VA Set velocity ♦ ♦ ♦ 3- 145
VB Set base velocity for step motors ♦ ♦ ♦ 3- 146
VU Set maximum speed ♦ ♦ ♦ 3- 149

FLOW CONTROL & SEQUENCING
DL Define label ♦ 3- 50
JL Jump to label ♦ ♦ 3- 86
RQ Generate service request ♦ ♦ ♦ 3- 120
SA Set device address ♦ ♦ ♦ 3- 122
WP Wait for absolute position
crossing
♦ ♦ ♦ 3- 150
WS Wait for stop ♦ ♦ ♦ 3- 151
WT Wait for time ♦ ♦ ♦ 3- 152

I/O FUNCTIONS
BG Assign DIO bits to execute stored programs ♦ ♦ 3- 32
BK Assign DIO bits to inhibit motion ♦ ♦ ♦ 3- 33
BL Enable DIO bits to inhibit motion ♦ ♦ ♦ 3- 34
BM Assign DIO bits to notify motion status ♦ ♦ ♦ 3- 35
BN Enable DIO bits to notify motion status ♦ ♦ ♦ 3- 36
BO Set DIO Port Direction ♦ ♦ ♦ 3- 37
BP Assign DIO for jog mode ♦ ♦ ♦ 3- 38
BQ Enable/disable DIO jog mode ♦ ♦ ♦ 3- 39
DC Setup data acquisition ♦ ♦ 3- 43
DD Get data acquisition done status ♦ ♦ 3- 45
DE Enable/disable data acquisition ♦ ♦ 3- 46
DF Get data acquisition sample count ♦ ♦ 3- 47
DG Get acquisition data ♦ ♦ 3- 48
SB Set DIO state ♦ ♦ ♦ 3- 123
UL Wait for DIO bit low ♦ 3- 144
UH Wait for DIO bit high ♦ 3- 143

GROUP FUNCTIONS
HA Set group acceleration ♦ ♦ ♦ 3- 61
HB Read list of groups assigned ♦ ♦ 3- 63
HC Move group along an arc ♦ ♦ ♦ 3- 64
HD Set group deceleration ♦ ♦ ♦ 3- 66
HE Set group E-stop deceleration ♦ ♦ ♦ 3- 68
HF Group motor power OFF ♦ ♦ ♦ 3- 69
HJ Set group jerk ♦ ♦ ♦ 3- 70
HL Move group along a line ♦ ♦ ♦ 3- 71
HN Create new group ♦ ♦ 3- 73
HO Group motor power ON ♦ ♦ ♦ 3- 75
HP Get group position ♦ ♦ 3- 76
HQ Wait for group via point buffer
near empty ♦ ♦ ♦ 3- 77
HS Stop group motion ♦ ♦ ♦ 3- 78
HV Set group velocity ♦ ♦ ♦ 3- 79
HW Wait for group motion to stop ♦ ♦ ♦ 3- 80
HX Delete a group ♦ ♦ ♦ 3- 81
HZ Get group size ♦ ♦ 3- 82

DIGITAL FILTERS
AF Acceleration/Deceleration feedforward gain ♦ ♦ ♦ 3- 26
CL Set closed loop update interval ♦ ♦ ♦ 3- 40
DB Set position deadband ♦ ♦ ♦ 3- 42
KD Set derivative gain Kd ♦ ♦ ♦ 3- 88
KI Set integral gain Ki ♦ ♦ ♦ 3- 89
KP Set proportional gain Kp ♦ ♦ ♦ 3- 90
KS Set saturation coefficient Ks ♦ ♦ ♦ 3- 91
UF Update Filter Parameters ♦ ♦ ♦ 3- 142
VF Set velocity feed-forward gain ♦ ♦ ♦ 3- 148


MASTER-SLAVE MODE DEFINITION
GR Set master-slave Ratio ♦ ♦ ♦ 3- 60
SI Set master-slave jog update interval ♦ ♦ ♦ 3- 126
SK Set slave axis jog velocity coefficients ♦ ♦ ♦ 3- 127
SS Set master-slave mode ♦ ♦ 3- 132

'''