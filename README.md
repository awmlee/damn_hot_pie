# Raspberry Pi Temperature Humidity (DHT sensor) + Air Quality Sensor (Plantower PMSx003) Website App
This app lets you to view Temperature and Humidity (DHT readouts) and PM1, PM2.5, and PM10 Air Quality Index values (Plantower PMS7003 sensor) online in a form of interactive plot hosted from your Raspberry Pi.  This is a modification of the damn_hot_pie (from mwmajewsk) which hadn't been updated since 2015.  I added the ability to log and plot AQI so that I could monitor indoor air quality during the 2020 California wildfires.  Using this setup, I was able to check the effectiveness of my air filters -- since I'm stuck at home all day b/c COVID-19.

This same raspberry pi also runs an RPi Camera server on another webpage, so it's doing a lot of work.     

Sample:

![alt text](https://github.com/awmlee/damn_hot_pie/blob/master/Capture.PNG "Sample of what it looks like")

(Viewing this plot may require you to push the autoscale button on plot.)

###Setup
- Raspberry PI
- DHT11 sensor (DHT22 and DHT2303 are also supported, [also see wiring](http://docs.gadgetkeeper.com/pages/viewpage.action?pageId=7700673)) 
- PMS7003 sensor (added for this version)
- interwebz connection
- Python >3
- Flask
- SQLAlchemy (must use pip3 install flask-sqlalchemy==2.1.0 -- newer version will fail)
- Adafruit DHT driver
- plotly 

##Dependencies
For web server and database dependencies requirements run:
```
pip3 install Flask
pip3 install SQLAlchemy
pip3 install flask-sqlalchemy==2.1.0
pip3 install Adafruit_DHT
pip3 install pms7003 
```

You will also need Adafruit Python DHT driver. 
The driver is accessible here:
https://github.com/adafruit/Adafruit_Python_DHT 
Follow the installation instructions in the link above.

##Installation

This projects runs purely as python app. As long as all the requirements are met, you don't have to install anything.

##Running the project
If you are not interested in further options just run:
```
python run_app.py
```
Website will run defaultly on host `0.0.0.0` and port `8080`.

##Additional options of running and project files

###model.py
This file contains sql model of the database where all sensor data will be saved. Running this script will result in creating file `dht_database.db` in folder where `model.py` is.

###record_data.py and recording data to database
Contains class responsible for acquiring data input and saving it in database. Can be runned separately as script. If run, will loop endlessly and save sensor data to database with given interval.  (Note 2020:  This is currently hard coded for DHT11 as the previous version wasn't running)

```
Usage: record_data.py [options]

Options:
  -h, --help  show this help message and exit
  -p          print every record to STDOUT [default: False]
  -t T        time interval in minutes to request readout from sensor
              [default: 15]
  --pin=PIN   data pin connected to sensor [default: 4]
  -s S        number of DHT sensor in use (supported: 11, 22, 2302) [default:
              11]
```


###server.py, template/index.html and the web service
`server.py` contains flask server with web-service. The web-service hosts restful api.

Method | Endpoint | Usage | Returns
---------- | ------------- | ------------- | -------------
GET | /data/ | Get last n sensor data rows. Where n is limit given in script. | List of sensor readouts.
GET | /data/{m} | Get last m sensor data rows. Where m is given parameter. If m>n then service will return n data rows. Where n is limit given in script.  | List of sensor readouts.
GET | /last | Get last sensor readout. |  Sensor readout.

Sensor readout(JSON):
```
{"date": "Y-M-D h:m:s.s", "id": id, "temperature": t, "humidity": h}
```

Example:
```
{"date": "2015-09-12 11:23:25.126321", "id": 3, "temperature": 20, "humidity": 37}
```

Request send to `/` will return index page from template folder.

`server.py` can be runned separately as a script. If so, it will set up web-service defaultly on host `0.0.0.0` and port `8080`.

```
Usage: server.py [options]

Options:
  -h, --help   show this help message and exit
  --port=PORT  port [default: 8080]
  --host=HOST  host [default: 0.0.0.0]
  -n N         max limit of rows available by /data/ [default: 100]
```


###run_app.py
(Note 2020:  This is untested.  I run 
python3 record_data.py -p &
and
python3 server.py &)

This script combines run of `service.py` and `record_data.py`.
The recording class from `record_data.py` runs as a separate thread.
```
Usage: you can find options info in server.py and record_data.py or by calling this script with -h options

Options:
  -h, --help   show this help message and exit
  --port=PORT  port [default: 8080]
  --host=HOST  host [default: 0.0.0.0]
  -n N         max limit of rows available by /data/ [default: 100]
  -p           print every record to STDOUT [default: False]
  -t T         time interval in minutes to request readout from sensor
               [default: 15]
  --pin=PIN    data pin connected to sensor [default: 4]
  -s S         number of DHT sensor in use (supported: 11, 22, 2302) [default:
               11]
```
