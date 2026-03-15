#!/usr/bin/env python3
import base64
import json
import sys
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

def recognize_image(image_path):
    try:
        # 读取图片并Base64编码
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 从环境变量获取密钥
        secret_id = os.environ.get('TENCENTCLOUD_SECRET_ID')
        secret_key = os.environ.get('TENCENTCLOUD_SECRET_KEY')
        
        if not secret_id or not secret_key:
            print("错误：需要设置TENCENTCLOUD_SECRET_ID和TENCENTCLOUD_SECRET_KEY环境变量")
            return None
        
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        req = models.GeneralBasicOCRRequest()
        params = {
            "ImageBase64": image_base64
        }
        req.from_json_string(json.dumps(params))

        resp = client.GeneralBasicOCR(req)
        result = json.loads(resp.to_json_string())
        
        # 提取识别结果
        texts = []
        for item in result['TextDetections']:
            texts.append(item['DetectedText'])
        
        return texts

    except TencentCloudSDKException as err:
        print(f"OCR识别错误: {err}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ocr_tencent.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = recognize_image(image_path)
    if result:
        print("识别结果:")
        print("=" * 50)
        for text in result:
            print(text)
