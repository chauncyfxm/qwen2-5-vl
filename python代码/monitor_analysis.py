import cv2
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from modelscope.hub.snapshot_download import snapshot_download  


# 初始化视频捕获（默认摄像头）
cap = cv2.VideoCapture(0)

# 加载模型（使用ModelScope下载）
model_dir = snapshot_download('qwen/Qwen2.5-VL-3B-Instruct')
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_dir, 
    device_map="auto",
    attn_implementation="flash_attention_2",
    torch_dtype="auto"
)
processor = AutoProcessor.from_pretrained(model_dir,max_pixels=1280*28*28)

# 实时分析函数
def frame_to_base64(frame):
    """将OpenCV帧转换为base64字符串"""
    _, buffer = cv2.imencode('.jpg', frame)
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode()

def realtime_analysis(img_base64):
    """通用分析函数（接受任意base64图像输入）"""
    # 构建消息格式
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": img_base64},
            {"type": "text", "text": "实时监控画面分析：检测当前画面中的异常情况，包括人员入侵、物品遗留、火灾烟雾等危险因素。"}
        ]
    }]
    
    # 预处理输入
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        padding=True,
        return_tensors="pt"
    ).to(model.device)
    
    # 生成分析结果
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

# 监控循环
def monitor_loop(model, processor, cap):
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 外部转换后传入
            img_base64 = frame_to_base64(frame)
            analysis_result = realtime_analysis(img_base64)
            print(f"检测结果：{analysis_result}")
            
            cv2.imshow('Monitor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("\n监控已终止")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    monitor_loop(model, processor, cap)