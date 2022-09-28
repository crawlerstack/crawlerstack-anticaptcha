# crawlerstack-anticaptcha

anticaptcha api service

### build and run

- 先开启MySQL服务容器，再使用 `docker-compose` 构建运行应用服务
    - 开启MySQL容器

        ```base
        docker run -e MYSQL_ROOT_PASSWORD=[password] -e MYSQL_DATABASE=[database] -p 3307:3306 --network db --name mysql mysql:debian
        ```
    - 再执行 `docker compose up` 构建应用容器

### 数据库迁移

开启服务前使用命令升级本地对应数据库

```base
alembic upgrade head 
```