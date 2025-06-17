FROM python:3.9-slim

# 安装 libcurl，这是 pycurl 的系统依赖
RUN apt-get update && apt-get install -y libcurl4-openssl-dev libssl-dev

WORKDIR /app

COPY requirements.txt .
# 使用 --no-cache-dir 可以减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
