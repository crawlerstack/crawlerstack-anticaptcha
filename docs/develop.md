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

- poet 请求

```base
url = "***/crawlerstack/captcha/identify/"

payload={'category': 'SliderCaptcha'}
files=[
  ('file',('foo.jpg',open('image path','rb'),'image/jpeg'))
]

response = requests.post(url, data=payload, files=files)
```

- put 请求

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
        "file_id": "f1261966-406b-11ed-a416-0242ac140002",
        "value": 242,
        "category": "SliderCaptcha"
    },
    "message": "File parsing succeeded."
}
```

put 返回值

```json
{
    "code": 200,
    "data": null,
    "message": "Update file id is the \"success\"=True of f1261966-406b-11ed-a416-0242ac140002."
}
```

### 数据库表结构

- category

| id  |     name      | path |
|:---:|:-------------:|:----:|
|  1  | SliderCaptcha | Path |

- captcha

| id  | file_id | category | file_type | creation_time | success |
|:---:|:-------:|:--------:|:---------:|:-------------:|:-------:|
|  1  |  uuid   |    1     |    jpg    |    2022...    |  NULL   |  

## 注意：

### opencv

- 构建docker后，运行报错：`ImportError: libGL.so.1: cannot open shared object file: No such file or directory`

  opencv在docker环境下使用无需 GUI 库依赖项，
  所以使用 `pip install opencv-python-headless`  [无头主模块包](https://pypi.org/project/opencv-python-headless/)
  或 `opencv-contrib-python-headless`Headless 完整包 安装

### docker部署

先开启MySQL服务容器，再使用 `docker-compose` 构建运行应用服务
开启MySQL容器

```base
docker run -e MYSQL_ROOT_PASSWORD=[password] -e MYSQL_DATABASE=[database] -p 3307:3306 --network db --name mysql mysql:debian
```

再执行构建应用容器

```base
docker compose build
docker compose up
```

### 数据库迁移（使用alembic）

生成本地初始化脚本

```base
alembic revision -m "init_db"
```

更新数据库版本

```base
alembic upgrade head 
```

生成迁移代码

```base
alembic revision --autogenerate -m "init_table"
```

其中需要初始化写入的数据需手动补充

```base
category_table = op.create_table('category',)...
...
    op.bulk_insert(
        category_table,
        [
            {
                "name": "SliderCaptcha",
                "path": str(Path(settings.IMAGE_SAVE_PATH).joinpath(Path('slider-captcha')))
            },
            {
                "name": "RotatedCaptcha",
                "path": str(Path(settings.IMAGE_SAVE_PATH).joinpath(Path('rotated-captcha')))
            }
        ]
    )
```

最后执行升级`upgrade`命令将数据库升级到最新

```base
alembic upgrade head 
```
