import cv2
import os
from vision_analyzer import init_models, realtime_analysis, frame_to_base64

# 初始化模型
try:
    model, processor = init_models()
    print("模型初始化成功")
except Exception as e:
    print(f"模型初始化失败: {e}")
    exit(1)

# 图像路径处理
try:
    img_path = os.path.join(os.path.dirname(__file__), 'test.jpg')
    frame = cv2.imread(img_path)
    if frame is None:
        raise FileNotFoundError(f"未找到图像文件: {img_path}")

except Exception as e:
    print(f"文件加载错误: {e}")
    exit(1)

# 执行分析
try:
    img_base64 = frame_to_base64(frame)
    result = realtime_analysis(img_base64)
    print("\n分析结果:")
    print(result.replace("\\", ""))  # 移除转义字符

except Exception as e:
    print(f"分析过程中出现异常: {e}")

# 清理资源
cv2.destroyAllWindows()