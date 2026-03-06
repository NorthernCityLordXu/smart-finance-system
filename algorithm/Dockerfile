# 1. 使用官方的轻量级 Python 3.12 镜像作为基础环境
FROM python:3.12-slim

# 2. 设置容器内的工作目录（相当于在容器里建了个 /app 文件夹并 cd 进去）
WORKDIR /app

# 3. 把你本机 algorithm 目录下的所有文件，复制到容器的 /app 里
COPY . /app

# 4. 使用清华源安装你代码里用到的依赖库（完美绕过网络代理问题）
RUN pip install fastapi uvicorn pydantic pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 5. 声明容器将对外暴露 8000 端口
EXPOSE 8000

# 6. 容器启动时执行的终极命令（相当于你手动敲的运行命令）
# 注意这里 host 必须是 0.0.0.0，这样别的容器才能访问到它
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]