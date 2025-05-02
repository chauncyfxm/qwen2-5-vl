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

    processor = AutoProcessor.from_pretrained(
        model_dir
    )
    return model, processor

def realtime_analysis(img_base64,processor , model):
    """通用图像分析函数
    参数：
        img_base64: 符合data:image/jpeg;base64格式的字符串
    """
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", 
            "image": "data:image/jpeg;base64," + img_base64,
            "resized_height": 1080/8,
            "resized_width": 1920/8
            },
            {"type": "text", "text": "找出(所有的)带血条的单位,单位的位置,整个图片大小也显示出来,要求包含以下字段：\n1. 血条颜色（中文）\n2. 坐标位置[x1,y1,x2,y2]\n3. 图片大小\n。例如：[{\"血条颜色\": \"红\", \"坐标位置\": [10,10,20,20], \"图片大小\": [1920,1080]}]"}
        ]
    }]
    image_inputs, video_inputs = process_vision_info(messages)
    text = processor.apply_chat_template(
        messages, 
        tokenize=False,
        add_generation_prompt=True
        )
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
    print("开始: ")
    #测试一下功能
    model,prossesor = init_models()

    import base64
    try:
        with open('C:\\Users\\chauncyfxm\\Desktop\\Qwen2.5-VL\\python代码\\test.jpg', 'rb') as f:
            jpg_data = f.read()
        print("文件读取成功")
        img_base64 = base64.b64encode(jpg_data).decode()
    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
    except Exception as e:
        print(f"发生了其他错误: {e}")



    string = realtime_analysis(img_base64, prossesor, model)
    print(string)

    