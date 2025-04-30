import win32gui
import win32ui
import win32con
import win32api
import ctypes
from ctypes import wintypes
import time
import threading
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class WatermarkOverlay:
    def __init__(self):
        self.hwnd = None
        self.running = False
        self.thread = None
        self.watermark_text = "机密文件"

    def set_watermark_text(self, text):
        self.watermark_text = text
        self.font_size = 36

    def set_font_size(self, size):
        self.font_size = size
        self.text_color = (200, 200, 200, 128)  # RGBA

    def set_text_color(self, color):
        self.text_color = color
        self.position = "tl"  # tl, tr, bl, br, center

    def set_position(self, position):
        self.position = position
        self.follow_mouse = False

    def set_follow_mouse(self, follow):
        self.follow_mouse = follow
        self.show_timestamp = True

    def set_timestamp(self, show):
        self.show_timestamp = show
        self.hook_installed = False
        
    def _create_transparent_window(self):
        """创建透明窗口"""
        # 注册窗口类
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "WatermarkOverlay"
        wc.lpfnWndProc = self._window_proc
        class_atom = win32gui.RegisterClass(wc)
        
        # 创建窗口
        self.hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
            class_atom,
            "WatermarkOverlay",
            win32con.WS_POPUP,
            0, 0, 0, 0,
            None, None, wc.hInstance, None
        )
        
        # 设置窗口为透明
        win32gui.SetLayeredWindowAttributes(
            self.hwnd, 0, 255, win32con.LWA_ALPHA
        )
        
        # 设置窗口为点击穿透
        ctypes.windll.user32.SetWindowLongW(
            self.hwnd, -20, 
            ctypes.windll.user32.GetWindowLongW(self.hwnd, -20) | 0x80000 | 0x20
        )
        
        # 显示窗口
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        
        # 获取屏幕尺寸
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        # 创建缓冲图像
        self.buffer = np.zeros((self.screen_height, self.screen_width, 4), dtype=np.uint8)
    
    def _window_proc(self, hwnd, msg, wparam, lparam):
        """窗口过程函数"""
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def _draw_watermark(self):
        """绘制水印到缓冲区"""
        try:
            # 创建PIL图像
            img = Image.fromarray(self.buffer, 'RGBA')
            draw = ImageDraw.Draw(img)
            
            # 加载字体
            try:
                font = ImageFont.truetype("arial.ttf", self.font_size)
            except:
                font = ImageFont.load_default().font_variant(size=self.font_size)
            
            # 准备文本
            text_parts = []
            if self.show_timestamp:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                text_parts.append(timestamp)
                text_parts.append("\n")
            text_parts.append(self.watermark_text)
            full_text = "\n".join(text_parts)
            
            # 计算文本大小
            left, top, right, bottom = draw.textbbox((0, 0), full_text, font=font)
            text_width = right - left
            text_height = bottom - top
            
            # 确定位置
            if self.position == "tl":  # 左上
                x, y = 20, 20
            elif self.position == "tr":  # 右上
                x, y = self.screen_width - text_width - 20, 20
            elif self.position == "bl":  # 左下
                x, y = 20, self.screen_height - text_height - 20
            elif self.position == "br":  # 右下
                x, y = self.screen_width - text_width - 20, self.screen_height - text_height - 20
            else:  # center
                x, y = (self.screen_width - text_width) // 2, (self.screen_height - text_height) // 2
            
            # 如果跟随鼠标
            if self.follow_mouse:
                mouse_x, mouse_y = win32api.GetCursorPos()
                x, y = mouse_x + 20, mouse_y - text_height - 20
            
            # 确保在屏幕范围内
            x = max(0, min(x, self.screen_width - text_width))
            y = max(0, min(y, self.screen_height - text_height))
            
            # 绘制半透明文字
            draw.text((x, y), full_text, font=font, fill=self.text_color)
            
            # 将PIL图像转换回numpy数组
            self.buffer = np.array(img)
        except Exception as e:
            print(f"绘制水印时出错: {e}")
    
    def _update_screen(self):
        """更新屏幕显示"""
        try:
            # 创建DC
            hdc = win32gui.GetDC(self.hwnd)
            mdc = win32ui.CreateDCFromHandle(hdc)
            save_dc = mdc.CreateCompatibleDC()
            
            # 创建位图
            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mdc, self.screen_width, self.screen_height)
            save_dc.SelectObject(save_bitmap)
            
            # 将numpy数组转换为位图
            # 注意：这里简化了处理，实际需要将RGBA转换为BGRA并处理alpha通道
            # 完整实现需要更复杂的颜色空间转换
            # 这里仅作为演示
            if self.buffer is not None:
                # 这里应该有更复杂的转换代码
                pass
            
            # 显示（简化版）
            # 实际上应该使用UpdateLayeredWindow来更新窗口内容
            # 完整实现需要更多代码
            
            # 释放资源
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hdc)
        except Exception as e:
            print(f"更新屏幕时出错: {e}")
    
    def start(self):
        """开始显示水印"""
        if self.running:
            return
            
        self._create_transparent_window()
        self.running = True
        self.thread = threading.Thread(target=self._overlay_loop)
        self.thread.daemon = True
        self.thread.start()
        print("水印已启动")
    
    def _overlay_loop(self):
        """水印叠加主循环"""
        try:
            last_update = 0
            while self.running:
                current_time = time.time()
                
                # 每0.5秒更新一次水印内容
                if current_time - last_update > 0.5:
                    self._draw_watermark()
                    last_update = current_time
                
                # 每10毫秒更新一次屏幕显示
                # 实际上应该使用更高效的方法，如等待垂直同步
                time.sleep(0.01)
        except Exception as e:
            print(f"水印循环出错: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """停止显示水印"""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        
        if self.hwnd:
            win32gui.DestroyWindow(self.hwnd)
            self.hwnd = None
        
        print("水印已停止")

# 使用示例
if __name__ == "__main__":
    watermark = WatermarkOverlay()
    watermark.set_watermark_text("内部机密")
    watermark.set_font_size(40)
    watermark.set_text_color((255, 0, 0, 150))  # 红色，半透明
    watermark.set_position("tr")  # 右上角
    watermark.set_timestamp(True)
    watermark.set_follow_mouse(False)
    
    watermark.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watermark.stop()