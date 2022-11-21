# crawlerstack-anticaptcha

anticaptcha api service

## 部署指南

### docker部署

先开启MySQL服务容器，再使用 `docker-compose` 构建运行应用服务

```bash
# 开启MySQL容器:
docker run -e MYSQL_ROOT_PASSWORD=[password] -e MYSQL_DATABASE=[database] -p 3307:3306 --network db --name mysql mysql:debian
```

再执行构建应用容器

```bash
docker compose build
docker compose up
```

### 数据库迁移（使用alembic）

根据迁移脚本，将数据库升级到最新

```bash
alembic upgrade head
```

## 接口介绍

| 操作       | Action | api                                      | 说明                  |
|----------|:------:|:-----------------------------------------|:--------------------|
| 查询验证码分类  |  GET   | /v1/api/captcha/categories               | 所有分类查询              |
| 添加验证码分类  |  POST  | /v1/api/captcha/categories               | 新增验证码分类             |
| 修改验证码分类  | PATCH  | /v1/api/captcha/categories/{category_id} | 基于id修改验证码分类         |
| 识别接口     |  POST  | /v1/api/captcha/identify/                | 根据请求参数，识别对应验证码，返回结果 |
| 回调接口     | PATCH  | /v1/api/captcha/record/{record_id}       | 将识别结果成功的事件状态改为成功    |
| 查询存储配置   |  GET   | /v1/api/captcha/storages                 | 所有存储分类查询            |
| 添加存储配置   |  POST  | /v1/api/captcha/storages                 | 新增存储配置              |
| 获取存储配置详情 |  GET   | /v1/api/captcha/storages/{id}            | 查询指定id的详情           |
| 修改存储配置   | PATCH  | /v1/api/captcha/storages/{id}            | 基于id修改              |
