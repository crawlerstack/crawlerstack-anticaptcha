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

验证码实例网站

- 数字字母混合 [中国知网](http://my.cnki.net/elibregister/commonRegister.aspx)
- 滑块验证码
    - [海关数据网站](http://43.248.49.97/);
    - [https://dun.163.com/trial/jigsaw](https://dun.163.com/trial/jigsaw)

## 接口调用

### 识别接口

- 接口描述

```text
根据请求参数，识别对应验证码，返回结果
```

- 请求url
  `/v1/api/captcha/identify/`

- 请求方式
  `post`

- 输入示例

```json
{
  "category_id": 1001,
  "image": "识别图的base64字符串",
  "fore_image": "前景图片base64字符串",
  "extra_content": "点选文字"
}
```

- 返回示例

```json
{
  "code": 10000,
  "message": "ok",
  "data": {
    "record_id": 123456789,
    "category_id": 1001,
    "result": 1234
  }
}
```

### 回调接口

- 简单描述

```text
将识别结果成功的事件状态改为成功
```

- 请求url
  `/v1/api/captcha/record/{record_id}`

- 请求方式
  `PATCH`

- 输入示例

```json
{
  "success": true
}
```

- 返回示例：

```json
{
  "code": 10000,
  "message": "ok"
}
```

### 验证码分类接口

| 操作       | Action | api                                      | 说明                  |
|----------|:------:|:-----------------------------------------|:--------------------|
| 查询验证码分类  |  GET   | /v1/api/captcha/categories               | 所有分类查询              |
| 添加验证码分类  |  POST  | /v1/api/captcha/categories               | 新增验证码分类             |
| 修改验证码分类  | PATCH  | /v1/api/captcha/categories/{category_id} | 基于id修改验证码分类         |

- 返回示例

添加/修改/删除验证码响应：

```json
{
  "code": 10000,
  "message": "ok"
}
```

- 验证码分类响应

```json
{
  "code": 10000,
  "message": "ok",
  "data": [
    {
      "id": 1001,
      "name": "滑动验证码"
    },
    {
      "id": 1002,
      "name": "旋转验证码"
    }
  ]
}
```

### 存储配置接口

| 操作       | Action | api                                      | 说明                  |
|----------|:------:|:-----------------------------------------|:--------------------|
| 查询存储配置   |  GET   | /v1/api/captcha/storages                 | 所有存储分类查询            |
| 添加存储配置   |  POST  | /v1/api/captcha/storages                 | 新增存储配置              |
| 获取存储配置详情 |  GET   | /v1/api/captcha/storages/{id}            | 查询指定id的详情           |
| 修改存储配置   | PATCH  | /v1/api/captcha/storages/{id}            | 基于id修改              |

- 返回示例：

添加/修改/删除存储配置响应

```json
{
  "code": 10000,
  "message": "ok"
}
```

获取存储配置响应

```json
{
  "code": 10000,
  "message": "ok",
  "data": {
    "id": 1,
    "name": "名称",
    "uri": "URI路径"
  }
}
```

查询存储配置响应

```json
{
  "code": 10000,
  "message": "ok",
  "data": [
    {
      "id": 1,
      "name": "名称",
      "uri": "URI路径"
    },
    {
      "id": 2,
      "name": "名称",
      "uri": "URI路径"
    }
  ]
}
```

## 数据库表结构

- captcha_category

| id   | name | update_time | create_time |
|------|------|-------------|-------------|
| 1001 | foo  | 2022...     | 2022...     |

- captcha_file

| id  | record_id | filename | file_type | storage_id | file_mark        | update_time | create_time |
|-----|-----------|----------|-----------|------------|------------------|-------------|-------------|
| 1   | 1         | uuid     | png       | 1          | Background image | 2022...     | 2022...     |

- captcha_record

| id  | category_id | content       | result | success | deleted | update_time | create_time |
|-----|-------------|---------------|--------|---------|---------|-------------|-------------|
| 1   | 1           | extra_content | foo    | true    | false   | 2022...     | 2022...     |

- storage

| id  | uri             | name  | default | update_time | create_time |
|-----|-----------------|-------|---------|-------------|-------------|
| 1   | localfile: //... | local | true    | 2022...     | 2022...     |

## 注意：

### opencv

- 构建docker后，运行报错：`ImportError: libGL.so.1: cannot open shared object file: No such file or directory`

opencv在docker环境下使用无需 GUI 库依赖项，
所以使用 `pip install opencv-python-headless`  [无头主模块包](https: //pypi.org/project/opencv-python-headless/)
或 `opencv-contrib-python-headless`Headless 完整包 安装

### docker部署

先开启MySQL服务容器，再使用 `docker-compose` 构建运行应用服务
开启MySQL容器

```base
docker run -e MYSQL_ROOT_PASSWORD=[password] -e MYSQL_DATABASE=[database] -p 3307: 3306 --network db --name mysql mysql:debian
```

再执行构建应用容器

```base
docker compose build
docker compose up
```

### 数据库迁移（使用alembic）

生成本地初始化脚本

```bash
alembic revision -m "init_db"
```

更新数据库版本

```bash
alembic upgrade head
```

生成迁移代码

```bash
alembic revision --autogenerate -m "init_table"
```

其中需要初始化写入的数据需手动补充

```
op.bulk_insert(
    category_table,
    [
        {
            'name': 'NumericalCaptcha',
            'id': 1001,
            'update_time': '2022-11-11 16:54:34',
            'create_time': '2022-11-11 16:54:34'
        },
        {
            'name': 'SliderCaptcha',
            'id': 1002,
            'update_time': '2022-11-17 10:54:34',
            'create_time': '2022-11-17 10:54:34'
        }
    ]
)
op.bulk_insert(
    storage_table,
    [
        {
            'name': 'local',
            'uri': f'localfile://{settings.CAPTCHA_IMAGE_PATH}',
            'default': True,
            'update_time': '2022-11-11 16:54:34',
            'create_time': '2022-11-11 16:54:34'
        }
    ]
)
```

最后执行升级`upgrade`命令将数据库升级到最新

```bash
alembic upgrade head
```