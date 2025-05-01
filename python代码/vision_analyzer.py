# -*- coding: utf-8 -*-
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from modelscope.hub.snapshot_download import snapshot_download


#attn_implementation="flash_attention_2",
def init_models():
    """初始化模型"""

    model_dir = snapshot_download('qwen/Qwen2.5-VL-3B-Instruct')
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_dir,
        torch_dtype="auto",
        attn_implementation="flash_attention_2",
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(model_dir)
    return model, processor

def realtime_analysis(img_base64,processor , model):
    """通用图像分析函数
    参数：
        img_base64: 符合data:image/jpeg;base64格式的字符串
    """
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": "data:image/jpeg;base64," + img_base64},
            {"type": "text", "text": "请以JSON格式输出图像分析结果，找出所有带血条的单位,要求包含以下字段：\n1. 血条颜色（中文）\n2. 坐标位置（x1,y1,x2,y2格式）\n3. 置信度（0-1）\n确保不使用转义字符，直接输出可解析的JSON。例如：[{\"血条颜色\": \"红\", \"坐标位置\": \"10,10,20,20\", \"置信度\": 0.9}]"}
        ]
    }]
    image_inputs, video_inputs = process_vision_info(messages)
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(
        text=[text],
        images=image_inputs,
        padding=True,
        return_tensors="pt"
    ).to(model.device)
    
    # 调用模型的generate方法进行文本生成，将之前处理好的输入参数解包传入，
    # 并设置生成的最大新标记数为128，最终得到生成的标记ID序列
    #, max_new_tokens=128
    generated_ids = model.generate(**inputs, max_new_tokens=9999999999999999999999)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]



if __name__ == "__main__":
    #测试一下功能
    model,prossesor = init_models()

    import base64
    try:
        with open('test.jpg', 'rb') as f:
            jpg_data = f.read()
        img_base64 = base64.b64encode(jpg_data).decode()
    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
    except Exception as e:
        print(f"发生了其他错误: {e}")



    string = realtime_analysis(img_base64, prossesor, model)
    print(string)

    