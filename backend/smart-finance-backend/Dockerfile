# 1. 使用官方的 Maven + JDK 17 镜像，自带全套 Java 编译环境
FROM maven:3.9-eclipse-temurin-21

# 2. 在容器里建一个 /app 工作目录
WORKDIR /app

# 3. 把你本机的 pom.xml 配置文件和 src 源码文件夹复制进容器
COPY pom.xml .
COPY src ./src

# 4. 在容器内部全自动执行 Maven 打包命令 (跳过测试以加快运行速度)
RUN mvn clean package -DskipTests

# 5. 声明暴露 8080 端口
EXPOSE 8080

# 6. 容器启动时，直接运行刚才打好的 jar 包
CMD ["sh", "-c", "java -jar target/*.jar"]