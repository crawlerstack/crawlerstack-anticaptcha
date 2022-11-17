# Build python distribute package.
FROM python:3.10 AS build

ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

RUN python -m pip  install -U pip  \
    && pip install  -U poetry

COPY . ./

RUN poetry build

FROM python:3.10

WORKDIR /app


RUN python -m pip install -U pip

COPY --from=0 /app/dist /app/dist

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  /app/dist/*.whl

EXPOSE 8000

ENTRYPOINT ["crawlerstack_anticaptcha"]
CMD ["api","-p","8000"]