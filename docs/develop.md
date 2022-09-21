# 验证码服务

## 需求

### 接口提供

- 用户传入验证码图像，返回识别结果
- 验证失败后的处理

### 破解填值类验证码

- 用户通过upload API接口上传验证码图片
- 使用相似度算法训练出已知数字（以及字母）的模型
- 验证码经过预处理后将图片中的每个字符进行拆分按照先后排序，再由相似度模型进行匹配得到内容返回值，提交到API接口

### 破解图像变换类验证码

两种情况

- 滑块验证，接收到验证码图片后，使用opencv计算缺口到边缘的距离
- 旋转验证，需要上传两张图片（即原图和需要旋转的图片）两图对比计算角度，通过网页中验证码滑块与旋转角度的比率关系计算出网页中滑块需要移动的距离

## 接口调用

poet 请求

```base
url = "***/crawlerstack/captcha/identify/"

payload={'category': 'SliderCaptcha'}
files=[
  ('file',('foo.jpg',open('image path','rb'),'image/jpeg'))
]

response = requests.post(url, data=payload, files=files)
```

put 请求

```base
url = "***/crawlerstack/captcha/record/[file-uuid]"

payload = json.dumps({
  "category": "SliderCaptcha",
  "success": True
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.put(url, headers=headers, data=payload)

```

### 接口返回值

post 返回值

```json
{
  "code": 200,
  "data": {
    "file_id": "bd107b6d-3987-11ed-a9cc-50ebf6777188",
    "value": 106,
    "category": "SliderCaptcha"
  },
  "message": "File parsing succeeded"
}
```

put 返回值

```json
{
  "file_id": "bd107b6d-3987-11ed-a9cc-50ebf6777188",
  "item": {
    "category": "SliderCaptcha",
    "success": true
  }
}
```
