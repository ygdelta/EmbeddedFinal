from flask import Flask, jsonify, render_template
from max30100 import MAX30100
from ds18b20 import DS18B20

app = Flask(__name__)

try:
    mx30 = MAX30100()
    mx30.begin()
except Exception as e:
    print("Init Error: %")

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
