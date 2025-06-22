# WebSocket 图片传输演示

这个项目演示了如何使用 Python WebSocket 实现图片传输系统。包含一个服务端（定时发送图片）和客户端（接收并保存图片）。
> ⚠️ **重要说明**  
> 本项目**仅为演示Websockets用途**。  
> **请勿直接将代码用于火柴人业务系统**，处理好可能发生的异常再投入使用，特别是客户端的保活（失败重试）。  
## 功能特性

- **服务端**：定时扫描指定目录下的图片文件并发送给所有连接的客户端
- **客户端**：接收图片并保存到本地目录，文件名包含时间戳防止重复
- **自动重连**：客户端在连接断开时会自动尝试重新连接
- **多客户端支持**：服务端可同时处理多个客户端连接

## 环境要求

- Python 3.11
- websockets 库

## 设置步骤

### 安装依赖
```
pip install websockets
```

### 项目结构
```
websocket-images-demo/
├── server.py            # 服务端脚本
├── client.py            # 客户端脚本
├── images/              # 服务端监控的图片目录
└── received_images/     # 客户端保存图片的目录
```

## 运行指南

### 启动服务端
```
python server.py [--host HOST] [--port PORT] [--dir IMAGE_DIR]

# 默认参数（推荐）
python server.py --host 0.0.0.0 --port 8765 --dir ./images
```
### 启动客户端
```
python client.py [--host SERVER_HOST] [--port SERVER_PORT] [--dir SAVE_DIR]

# 连接本地服务端
python client.py --host localhost --port 8765 --dir ./received_images
```
### 添加图片

将 JPG 或 PNG 格式图片放入服务端监控目录（默认为 ./images）

## 预期效果
### 服务端输出
```
启动WebSocket服务器 ws://0.0.0.0:8765
监控图片目录: ./images
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
客户端 127.0.0.1 已连接 (1 个在线)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
发送图片: msedge_g2NIyEU54K(1).png (1043860 字节)
```
### 客户端输出
```
连接到服务器: ws://localhost:8765
连接成功，等待接收图片...
图片已保存: image_20250622_150415_723246.jpg (1043860 字节)
图片已保存: image_20250622_150418_752075.jpg (1043860 字节)
图片已保存: image_20250622_150421_800764.jpg (1043860 字节)
图片已保存: image_20250622_150424_840866.jpg (1043860 字节)
图片已保存: image_20250622_150427_862689.jpg (1043860 字节)
```