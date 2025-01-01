from flask import Flask
from max30100 import MAX30100

app = Flask(__name__)

try:
    mx30 = MAX30100()
    mx30.begin()
except Exception as e:
    print("Init Error: %")

@app.route('/')
def home():
    return ""
