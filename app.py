from flask import Flask
import max30100

app = Flask(__name__)
try:
    mx30 = max30100.MAX30100()
except Exception as e:
    print("Init Error: %")

@app.route('/')
def home():
    return "<h1>Home Page</h1>"