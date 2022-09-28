# Build python distribute package.
FROM python:3.10 AS build

ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

RUN python -m pip --no-cache-dir install -U pip  \
    && pip install --no-cache-dir -U poetry

COPY . ./

RUN poetry build

# use playwright build image, and special playwright version.
# You should update it when update project to use.
FROM python:3.10

WORKDIR /app

COPY --from=0 /app/dist /app/dist

RUN python -m pip install -U pip \
    && pip install --no-cache-dir /app/dist/*.whl

EXPOSE 8080

ENTRYPOINT ["crawlerstack_anticaptcha"]
CMD ["api","-p","8000"]