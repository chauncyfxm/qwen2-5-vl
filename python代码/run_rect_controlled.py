import subprocess
import time
import psutil

exe_path = r'C:\Users\chauncyfxm\Desktop\Qwen2.5-VL\c++代码\rect_windows.exe'

for _ in range(1000):
    start_time = time.time()
    
    # 启动进程
    proc = subprocess.Popen(exe_path)
    
    # 等待进程初始化
    time.sleep(0.1)
    
    # 终止进程
    for process in psutil.process_iter():
        try:
            if process.exe().lower() == exe_path.lower():
                process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # 频率控制
    elapsed = time.time() - start_time
    sleep_time = max(0.0, 2 - elapsed)  # 确保每秒最多执行2次
    time.sleep(sleep_time)