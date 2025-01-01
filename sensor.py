import max30100

mx30 = max30100.MAX30100()
while 1:
    print(mx30.read_sensor())