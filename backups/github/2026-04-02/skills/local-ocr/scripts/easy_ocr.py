#!/usr/bin/env python3
import easyocr
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("使用方法：python easy_ocr.py 图片路径")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"错误：文件不存在 {image_path}")
        sys.exit(1)
    
    print("正在识别图片...")
    # 初始化OCR，支持中英文
    reader = easyocr.Reader(['ch_sim', 'en'])
    
    # 识别图片
    result = reader.readtext(image_path)
    
    print("\n识别结果：")
    print("="*50)
    for detection in result:
        text = detection[1]
        confidence = detection[2]
        print(f"[{confidence:.2f}] {text}")
    
    print("\n识别完成！")

if __name__ == "__main__":
    main()
