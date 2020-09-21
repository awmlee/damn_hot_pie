import time
from datetime import datetime
import adafruit_dht
import board
import threading
from model import db, DHTRecord
from optparse import OptionParser
import pms7003



#sensor_args = {	'11': Sensor.DHT11, '22': Sensor.DHT22, '2302': Sensor.AM2302}

def add_parser_options(parser):
	parser.add_option('-p', action="store_true", default=False, help="print every record to STDOUT [default: %default]")
	parser.add_option('-t', action="store", type="int", default=5, help="time interval in minutes to request readout from sensor [default: %default]")
	parser.add_option('--pin', dest="pin", action="store", type="int", default=18, help="data pin connected to sensor [default: %default]")
	parser.add_option('-s', action="store", type="str", default='11', help="number of DHT sensor in use (supported: 11, 22, 2302) [default: %default]")
	return parser


class SensorDatabase(threading.Thread):
	def __init__(self, pin, sensor_number, minutes_interval, print_to_stdout):
		self.pin = pin
		self.sensor_number = sensor_number
		self.minutes_interval = minutes_interval
		self.print_to_stdout = print_to_stdout
		threading.Thread.__init__(self)

	def record_to_database(self, data):
		humidity, temperature, PM1_0, PM2_5, PM10, datetime = data
		record = DHTRecord(humidity, temperature, PM1_0,PM2_5,PM10, datetime)
		db.session.add(record)
		db.session.commit()

	def run(self):
		dhtsensor=adafruit_dht.DHT22(board.D18)
		pmssensor=pms7003.Pms7003Sensor('/dev/serial0')
		while True:
			try:
				pms=pmssensor.read()
				data = dhtsensor.humidity, dhtsensor.temperature,pms["pm1_0"],pms["pm2_5"],pms["pm10"], datetime.now()
			except:
				print("sensor read error")
				time.sleep(sleep_time)
			else:
				self.record_to_database(data)
				one_minute = 60
				sleep_time = self.minutes_interval * one_minute
				#sleep_time=5
				if self.print_to_stdout:
					print(data)
				time.sleep(sleep_time)

if __name__ == "__main__":
	
	parser = OptionParser()
	praser = add_parser_options(parser)
	opts, args = parser.parse_args()
	#sensor = sensor_args[opts.s]
	sensor=1
	sd = SensorDatabase(opts.pin, sensor, opts.t, opts.p)
	sd.run()