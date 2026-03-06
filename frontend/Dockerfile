# ========== 阶段一：编译打包 ==========
# 1. 使用 Node.js 环境准备编译
FROM node:20-alpine AS build-stage

# 2. 在容器里建一个 /app 工作目录
WORKDIR /app

# 3. 先复制 package.json，并使用国内镜像极速安装依赖
COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com/ && npm install

# 4. 把所有前端代码复制进去，并执行打包命令 (会生成一个 dist 文件夹)
COPY . .
RUN npm run build


# ========== 阶段二：Nginx 部署 ==========
# 5. 使用轻量级的 Nginx 服务器
FROM nginx:alpine AS production-stage

# 6. 把阶段一里打包出来的 dist 文件夹，直接复制到 Nginx 的网页大本营里
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 7. 暴露 80 端口 (Web 默认端口)
EXPOSE 80

# 8. 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]