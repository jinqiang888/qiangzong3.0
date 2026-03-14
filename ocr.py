from paddleocr import PaddleOCR
import os

# 初始化OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 图片路径
img_path = r'C:\Users\Administrator\.openclaw\media\inbound\6cf23de4-4616-4dc4-a62d-eaf5c2640088.jpg'

# 识别
result = ocr.ocr(img_path, cls=True)

# 输出结果
for line in result:
    if line:
        for word in line:
            print(word[1][0])

