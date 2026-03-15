#!/usr/bin/env python3
import sys
import os
import base64
import requests

def recognize_image(image_path):
    """本地OCR识别，使用百度智能云免费接口"""
    # 首先尝试本地paddleocr
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        result = ocr.ocr(image_path, cls=True)
        texts = []
        for idx in range(len(result)):
            res = result[idx]
            if res:
                for line in res:
                    texts.append(line[1][0])
        return "\n".join(texts)
    except Exception as e:
        print(f"本地OCR失败: {e}，尝试在线接口...")
    
    # 备用：使用免费在线OCR接口
    try:
        with open(image_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        url = "https://api.textin.com/ai/service/v2/recognize"
        headers = {
            "x-ti-app-id": "7d2e6d5b8a9c0f1e2d3c4b5a6f7e8d9a",
            "x-ti-secret-code": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d",
            "Content-Type": "application/json"
        }
        data = {
            "image": img_base64,
            "type": "general"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if result.get("code") == 200:
            texts = []
            for line in result.get("result", {}).get("lines", []):
                texts.append(line.get("text", ""))
            return "\n".join(texts)
        else:
            return f"在线OCR失败: {result.get('message', '未知错误')}"
    
    except Exception as e:
        return f"所有OCR方式均失败: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ocr_local.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"错误：文件不存在 {image_path}")
        sys.exit(1)
    
    result = recognize_image(image_path)
    print("识别结果:")
    print("=" * 50)
    print(result)
