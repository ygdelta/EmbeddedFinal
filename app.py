from flask import Flask, jsonify, render_template
from max30100 import MAX30100
from ds18b20 import DS18B20
from mpu6050 import mpu6050

app = Flask(__name__)

try:
  mx30 = MAX30100()
  mx30.begin()
  ds18 = DS18B20()
  mpu6050 = mpu6050(0x68)
except Exception as e:
  print("Init Error: {}".format(e))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/max30100', methods=['GET'])
def getMax30100():
  res = jsonify({
    'heart_rate': mx30.heart_rate(),
    'spo2': mx30.spo2()
  })
  return res

@app.route('/ds18b20', methods=['GET'])
def getDS18B20():
  res = jsonify({
    'temperature': ds18.get_temperature()
  })
  return res

@app.route('/mpu6050', methods=['GET'])
def getMPU6050():
  accel_data = mpu6050.get_accel_data()
  status = 'normal'
  x = accel_data['x']
  y = accel_data['y']
  z = accel_data['z']
  if abs(z) > 5:
    status = 'danger'
  res = jsonify({
    'x': x,
    'y': y,
    'z': z,
    'status': status 
  })    
  return res