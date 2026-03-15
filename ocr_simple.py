#!/usr/bin/env python3
import sys
import os
import pytesseract
from PIL import Image

def recognize_image(image_path):
    """简单OCR识别，使用Tesseract"""
    try:
        # 打开图片
        img = Image.open(image_path)
        # 识别中文和英文
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        return text.strip()
    except Exception as e:
        return f"OCR识别失败: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ocr_simple.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"错误：文件不存在 {image_path}")
        sys.exit(1)
    
    result = recognize_image(image_path)
    print("识别结果:")
    print("=" * 50)
    print(result)
