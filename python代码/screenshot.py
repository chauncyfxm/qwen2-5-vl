import win32gui
import win32ui
import win32con
from PIL import Image
import pygetwindow
import io
import os


def get_all_window_titles():
    """获取所有非空标题的窗口名称列表"""
    windows = pygetwindow.getAllWindows()
    return [win.title for win in windows if win.title.strip()]


def capture_window(window_title):
    """根据窗口标题截取窗口画面"""
    windows = pygetwindow.getWindowsWithTitle(window_title)
    if not windows:
        raise ValueError(f"未找到标题包含 '{window_title}' 的窗口")
    
    win = windows[0]
    if win.isMinimized:
        win.restore()
    
    # 激活窗口确保内容渲染
    
    # 获取窗口句柄
    hwnd = win._hWnd
    
    # 获取窗口客户区尺寸
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bottom - top
    
    # 获取窗口设备上下文
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    
    # 使用PrintWindow捕获分层窗口内容
    import ctypes
    ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    
    # 添加延迟确保渲染完成
    win32gui.UpdateWindow(hwnd)
    win32gui.RedrawWindow(hwnd, None, None, win32con.RDW_UPDATENOW)
    
    # 转换为PIL图像
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    pil_img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )
    
    # 释放资源
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    
    return pil_img



def get_jpg_data(window_title):
    # 新增在try模块中的调用示例
    try:
        # 获取并打印所有窗口标题
        #print("当前所有窗口:", get_all_window_titles())
        
        # 原有截图代码保持不变
        #window_title = input("请输入要截取的窗口标题: ")

        screenshot = capture_window(window_title)
        
        # 转换为字节流
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='JPEG')
        jpg_data = img_byte_arr.getvalue()

        return jpg_data


    except ImportError as e:
        if "win32gui" in str(e):
            print("错误: 请先安装依赖库，执行命令: pip install pywin32")
        elif "PIL" in str(e):
            print("错误: 请先安装依赖库，执行命令: pip install Pillow")
        else:
            print(f"错误: 请先安装依赖库，执行命令: pip install pygetwindow")
    except Exception as e:
        print(f"操作失败: {str(e)}")

# 调试用保存（正式使用可注释）
if __name__ == "__main__":

    jpg_data = get_jpg_data()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, 'test.jpg')
    with open(save_path, 'wb') as f:
        f.write(jpg_data)
    print(f"调试文件已保存至: {save_path}")