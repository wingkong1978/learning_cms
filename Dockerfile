# 前端构建
FROM node:16 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# 后端构建
FROM python:3.9-slim
WORKDIR /app

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# 安装后端依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制后端代码
COPY backend /app/backend
COPY database /app/database

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "backend/app.py"] 