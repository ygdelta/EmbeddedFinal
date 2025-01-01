import smbus2
import time
import numpy as np
from collections import deque
from scipy.signal import find_peaks

class MAX30100:
    def __init__(self):
        self.address = 0x57
        self.bus = smbus2.SMBus(1)
        self.buffer_size = 200
        self.ir_buffer = deque(maxlen=self.buffer_size)
        self.red_buffer = deque(maxlen=self.buffer_size)
        self.time_buffer = deque(maxlen=self.buffer_size)
        self._is_initialized = False
        
    def begin(self):
        try:
            # 重置感測器
            self.bus.write_byte_data(self.address, 0x06, 0x40)
            time.sleep(0.1)
            
            # 設定工作模式
            self.bus.write_byte_data(self.address, 0x06, 0x03)  # HR + SpO2
            self.bus.write_byte_data(self.address, 0x07, 0x47)  # SpO2 設定
            self.bus.write_byte_data(self.address, 0x09, 0x24)  # LED 電流
            
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"初始化失敗: {e}")
            return False
    
    def update(self):
        if not self._is_initialized:
            return False
            
        try:
            data = self.bus.read_i2c_block_data(self.address, 0x05, 4)
            ir = (data[0] << 8) | data[1]
            red = (data[2] << 8) | data[3]
            
            if ir > 1000 and red > 1000:
                self.ir_buffer.append(ir)
                self.red_buffer.append(red)
                self.time_buffer.append(time.time())
            
            return True
        except:
            return False
    
    def heart_rate(self):
        if len(self.ir_buffer) < 100:
            return 0
            
        ir_data = np.array(list(self.ir_buffer))
        normalized_data = (ir_data - np.mean(ir_data)) / np.std(ir_data)
        
        peaks, _ = find_peaks(normalized_data, 
                            distance=20,
                            prominence=0.5)
        
        if len(peaks) < 2:
            return 0
            
        time_data = np.array(list(self.time_buffer))
        peak_times = time_data[peaks]
        intervals = np.diff(peak_times)
        
        if len(intervals) > 0:
            avg_interval = np.mean(intervals)
            heart_rate = 60 / avg_interval
            return int(min(180, max(30, heart_rate)))
        
        return 0
    
    def spo2(self):
        if len(self.ir_buffer) < 100:
            return 0
            
        ir_data = np.array(list(self.ir_buffer))
        red_data = np.array(list(self.red_buffer))
        
        window = 5
        ir_filtered = np.convolve(ir_data, np.ones(window)/window, mode='valid')
        red_filtered = np.convolve(red_data, np.ones(window)/window, mode='valid')
        
        ir_ac = np.ptp(ir_filtered)
        ir_dc = np.mean(ir_filtered)
        red_ac = np.ptp(red_filtered)
        red_dc = np.mean(red_filtered)
        
        if ir_dc == 0 or red_dc == 0:
            return 0
            
        r = (red_ac/red_dc)/(ir_ac/ir_dc)
        spo2 = 110 - 25 * r
        
        return int(min(100, max(80, spo2)))

# 使用範例
if __name__ == "__main__":
    sensor = MAX30100()
    
    print("初始化感測器...")
    if not sensor.begin():
        print("初始化失敗！")
        exit()
    
    print("請將手指放在感測器上")
    print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            sensor.update()
            hr = sensor.heart_rate()
            o2 = sensor.spo2()
            print(f"\r心率: {hr:3d} BPM | 血氧: {o2:3d}%", end="")
            time.sleep(0.01)
    except KeyboardInterrupt:
