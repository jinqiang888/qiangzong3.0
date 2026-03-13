---
name: local-ocr
description: 本地离线OCR文字识别，支持中英文，无需API密钥，完全免费。基于PaddleOCR，识别精度高，速度快。
---

# 本地OCR识别技能

## 用途
完全离线的图片文字识别，支持中英文、数字、符号，无需联网，无需API密钥。

## 能力
- 中英文混合识别
- 支持倾斜、模糊图片
- 返回识别文字和位置坐标
- 支持批量识别

## 依赖
```bash
pip install paddlepaddle paddleocr
```

## 使用方式
```bash
python scripts/ocr.py 图片路径
```
