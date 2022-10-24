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
