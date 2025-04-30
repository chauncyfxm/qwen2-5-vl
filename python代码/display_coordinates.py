import json
import tkinter as tk
from tkinter import Canvas

def load_coordinates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(f"data = json.load(file): {data}")
    
    coordinates = [item['坐标位置'] for item in data if '坐标位置' in item]
    print(f"coordinates: {coordinates}")
    return coordinates

def draw_bounding_boxes(canvas, coordinates):
    # 验证 coordinates 格式是否正确
    if not isinstance(coordinates, list) or not all(isinstance(coord, (list, tuple)) and len(coord) == 4 for coord in coordinates):
        raise ValueError("coordinates must be a list of lists/tuples with length 4")

    for coord in coordinates:
        if len(coord) != 4:
            raise ValueError(f"if len(coord) != 4:: {coord}")
        x1, y1, x2, y2 = coord
        print(f"x1, y1, x2, y2 = coord: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=2)

import win32gui
import win32con
def create_transparent_window():
    # 创建Tkinter窗口对象
    root = tk.Tk()
    # 设置窗口全屏
    root.attributes('-fullscreen', True)
    # 取消窗口置顶
    root.attributes('-topmost', True)
    # 去掉窗口边框和标题栏
    root.overrideredirect(True)
    # 将白色设置为透明色
    root.wm_attributes('-transparentcolor', 'white')
    # 创建一个画布，背景色设为白色，去掉边框
    canvas = Canvas(root, bg='white', highlightthickness=0)
    # 使画布填充整个窗口并随窗口大小变化
    canvas.pack(fill=tk.BOTH, expand=True)


    # 返回窗口和画布对象
    return root, canvas


def main():
    file_path = 'new_output.json'
    coordinates = load_coordinates(file_path)

    root, canvas = create_transparent_window()
    draw_bounding_boxes(canvas, coordinates)

    root.mainloop()

if __name__ == "__main__":
    main()