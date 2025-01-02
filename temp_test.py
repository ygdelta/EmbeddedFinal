import glob
import time

# 設定裝置目錄
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    """讀取感測器原始數據"""
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    """解析溫度數據"""
    lines = read_temp_raw()
    # 確認 CRC 校驗成功
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # 從第二行取得溫度數值
    temp_pos = lines[1].find('t=')
    if temp_pos != -1:
        temp_string = lines[1][temp_pos+2:]
        # 轉換到攝氏溫度
        temp_c = float(temp_string) / 1000.0
        return temp_c

# 主程式
try:
    while True:
        temperature = read_temp()
        print(f'溫度: {temperature:.2f}°C')
        time.sleep(1)
except KeyboardInterrupt:
    print('程式結束')
