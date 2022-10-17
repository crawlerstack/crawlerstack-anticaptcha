# crawlerstack-anticaptcha

anticaptcha api service

## 部署指南

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
            {
                "name": "NumericalCaptcha",
                "path": str(Path(settings.IMAGE_SAVE_PATH).joinpath(Path('numerical_captcha')))
            }
        ]
    )
```

最后执行升级`upgrade`命令将数据库升级到最新

```bash
alembic upgrade head
```