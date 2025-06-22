import asyncio
import websockets
import os
import time
import glob
import argparse

# 存储所有连接的客户端
CONNECTED_CLIENTS = set()

def parse_args():
    parser = argparse.ArgumentParser(description='WebSocket Image Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=8765, help='Port number')
    parser.add_argument('--dir', type=str, default='./images', help='Image directory')
    return parser.parse_args()

async def send_images(image_dir):
    """定时发送图片任务"""
    while True:
        # 获取目录中的所有图片文件
        image_files = glob.glob(os.path.join(image_dir, "*.jpg")) + \
                     glob.glob(os.path.join(image_dir, "*.png"))
        
        if not image_files:
            print("没有找到图片文件")
            await asyncio.sleep(5)
            continue
        
        # 遍历所有图片文件
        for image_path in image_files:
            try:
                # 读取图片二进制数据
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                
                # 发送图片给所有客户端
                filename = os.path.basename(image_path)
                print(f"发送图片: {filename} ({len(image_data)} 字节)")
                
                # 创建发送任务列表
                send_tasks = []
                for client in list(CONNECTED_CLIENTS):  # 避免在遍历时修改集合
                    try:
                        send_tasks.append(client.send(image_data))
                    except websockets.exceptions.ConnectionClosed:
                        # 连接已关闭的客户端
                        CONNECTED_CLIENTS.discard(client)
                        print(f"客户端断开 (清理)")
                
                if send_tasks:
                    await asyncio.gather(*send_tasks)
                
                await asyncio.sleep(3)  # 每张图片间隔3秒
                
            except Exception as e:
                print(f"发送图片出错: {e}")
                continue

async def handler(websocket):
    """处理客户端连接"""
    # 获取客户端IP地址
    remote_ip = websocket.remote_address[0] if websocket.remote_address else "unknown"
    
    # 添加到客户端集合
    CONNECTED_CLIENTS.add(websocket)
    print(f"客户端 {remote_ip} 已连接 ({len(CONNECTED_CLIENTS)} 个在线)")
    
    try:
        # 保持连接直到客户端断开
        async for message in websocket:
            # 可以添加心跳响应等逻辑
            print(f"收到客户端消息: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"客户端断开: {e}")
    finally:
        # 客户端断开时移除
        if websocket in CONNECTED_CLIENTS:
            CONNECTED_CLIENTS.remove(websocket)
        print(f"客户端 {remote_ip} 已断开 ({len(CONNECTED_CLIENTS)} 个在线)")

async def main():
    """启动服务器和定时任务"""
    args = parse_args()
    
    # 确保图片目录存在
    os.makedirs(args.dir, exist_ok=True)
    
    print(f"启动WebSocket服务器 ws://{args.host}:{args.port}")
    print(f"监控图片目录: {args.dir}")
    
    async with websockets.serve(handler, args.host, args.port):
        # 启动定时图片发送任务
        asyncio.create_task(send_images(args.dir))
        
        # 保持服务器运行
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())