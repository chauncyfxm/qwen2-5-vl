from PIL import Image

def read_and_show_image(image_path):
    """
    读取并显示指定路径的图片。

    :param image_path: 图片文件的路径
    """
    try:
        # 打开图片文件
        img = Image.open(image_path)
        

        return img
    
    except FileNotFoundError:
        print("错误：图片文件未找到。")
    except Exception as e:
        print(f"发生错误：{e}")
