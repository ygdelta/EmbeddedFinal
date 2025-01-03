from threading import Thread, Lock
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
        
        self._lock = Lock()
        self._current_hr = 0
        self._current_spo2 = 0
        self._running = False
        self._thread = None
    
    def begin(self):
        try:
            self.bus.write_byte_data(self.address, 0x06, 0x40)
            time.sleep(0.1)
            
            self.bus.write_byte_data(self.address, 0x06, 0x03)  # HR + SpO2
            self.bus.write_byte_data(self.address, 0x07, 0x47)  # SpO2 設定
            self.bus.write_byte_data(self.address, 0x09, 0x24)  # LED 電流
            
            self._running = True
            self._thread = Thread(target=self._update_thread, daemon=True)
            self._thread.start()
            
            return True
        except Exception as e:
            print(f"初始化失敗: {e}")
            return False
    
    def _update_thread(self):
        while self._running:
            try:
                data = self.bus.read_i2c_block_data(self.address, 0x05, 4)
                ir = (data[0] << 8) | data[1]
                red = (data[2] << 8) | data[3]
                
                if ir > 1000 and red > 1000:
                    with self._lock:
                        self.ir_buffer.append(ir)
                        self.red_buffer.append(red)
                        self.time_buffer.append(time.time())
                        
                        # 更新心率和血氧
                        self._current_hr = self._calculate_hr()
                        self._current_spo2 = self._calculate_spo2()
                
                time.sleep(0.01)  # 100Hz 採樣率
                
            except Exception as e:
                print(f"讀取錯誤: {e}")
                time.sleep(0.1)
    
    def _calculate_hr(self):
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
    
    def _calculate_spo2(self):
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
    
    def heart_rate(self):
        with self._lock:
            return self._current_hr
    
    def spo2(self):
        with self._lock:
            return self._current_spo2
    
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

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
            hr = sensor.heart_rate()
            o2 = sensor.spo2()
            print(f"\r心率: {hr:3d} BPM | 血氧: {o2:3d}%", end="")
            time.sleep(0.1)
    except KeyboardInterrupt:
        sensor.stop()
        print("\n程式結束")
