#!/usr/bin/env python3
from paddleocr import PaddleOCR
import sys

# 初始化OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 读取图片
img_path = sys.argv[1]
result = ocr.ocr(img_path, cls=True)

# 输出识别结果
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line[1][0])
