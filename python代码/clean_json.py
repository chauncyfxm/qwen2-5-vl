import re
import json


def extract_json_content(input_str = ['```json\n[\n\t{"bbox_2d": [0, 0, 6, 3], "label": "生 物"},\n\t{"bbox_2d": [270, 349, 697, 718], "label": "生物"}\n]\n```']):
    
    try :
        joined_str = ''.join(input_str)
    except :
        return
    pattern = re.compile(r'```json(.*?)```', re.DOTALL)
    match = pattern.search(joined_str)
    if match:
        json_content = match.group(1).strip()
        try:
            parsed_json = json.loads(json_content)
            with open('c:\\Users\\chauncyfxm\\Desktop\\Qwen2.5-VL\\new_output.json', 'w', encoding='utf-8') as f:
                json.dump(parsed_json, f, ensure_ascii=False, indent=4)
            print('JSON 内容已写入 new_output.json')
        except json.JSONDecodeError:
            print('提取的内容不是有效的 JSON 格式')
    else:
        print('未找到 JSON 内容')

if __name__ == '__main__':
    try:
        with open('c:\\Users\\chauncyfxm\\Desktop\\Qwen2.5-VL\\output.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        extract_json_content(data)
    except FileNotFoundError:
        print('未找到 output.json 文件')