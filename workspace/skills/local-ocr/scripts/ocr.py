#!/usr/bin/env python3
from paddleocr import PaddleOCR
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("使用方法：python ocr.py 图片路径")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"错误：文件不存在 {image_path}")
        sys.exit(1)
    
    # 初始化OCR，下载模型（第一次运行自动下载）
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    
    # 识别图片
    result = ocr.ocr(image_path, cls=True)
    
    # 输出结果
    print("识别结果：")
    print("="*50)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]
            confidence = line[1][1]
            print(f"[{confidence:.2f}] {text}")
    
    print("\n识别完成！")

if __name__ == "__main__":
    main()
