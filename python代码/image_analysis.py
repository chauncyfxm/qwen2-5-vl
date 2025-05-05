from vision_analyzer import init_models, realtime_analysis
import time
from screenshot import get_jpg_data, get_all_window_titles
from clean_json import extract_json_content
import base64



def analyze_image(processor, model,jpg_data):
    
    # 将图片转换为base64格式
    img_base64 = base64.b64encode(jpg_data).decode()
    print("# 将图片转换为base64格式 img_base64 = jpg_data_to_base64(jpg_data)我是第13行")
    # 使用Qwen2.5-VL模型进行分析
    analysis_result = realtime_analysis(img_base64,processor ,model)
    
    # 打印分析结果
    print("图像分析结果：")
    return analysis_result


#1111
# 初始化模型
model, processor = init_models()

# 指定图片路径
#image_path = 'C:\\Users\\chauncyfxm\\Desktop\\Qwen2.5-VL\\python代码\\test.jpg'

# 获取并打印所有窗口标题
print("当前所有窗口:", get_all_window_titles())

# 原有截图代码保持不变
window_title = input("请输入要截取的窗口标题: ")



while True:
    time.sleep(0.1)  # 延迟3秒
    # 调用函数分析图片
    jpg_data = get_jpg_data(window_title)
    print("jpg_data = get_jpg_data(window_title)我是41行")
    input_str = analyze_image(processor , model , jpg_data)

    #保存成json文件
    extract_json_content(input_str)

