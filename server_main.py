import asyncio
import websockets
import os
import time
import glob

# 存储所有连接的客户端
CONNECTED_CLIENTS = set()

async def send_images():
    """定时发送图片任务"""
    image_dir = "./images"  # 图片存储目录
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
                print(f"发送图片: {os.path.basename(image_path)}")
                if CONNECTED_CLIENTS:
                    await asyncio.gather(*[
                        client.send(image_data) 
                        for client in CONNECTED_CLIENTS
                    ])
                
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"发送图片出错: {e}")
                continue

async def handler(websocket, path):
    """处理客户端连接"""
    CONNECTED_CLIENTS.add(websocket)
    print(f"客户端已连接 ({len(CONNECTED_CLIENTS)} 个在线)")
    
    try:
        # 保持连接直到客户端断开
        async for message in websocket:
            pass  # 不需要处理客户端消息
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # 客户端断开时移除
        CONNECTED_CLIENTS.remove(websocket)
        print(f"客户端已断开 ({len(CONNECTED_CLIENTS)} 个在线)")

async def main():
    """启动服务器和定时任务"""
    server = await websockets.serve(handler, "0.0.0.0", 8765)
    print("WebSocket服务器已启动 ws://0.0.0.0:8765")
    
    # 启动定时图片发送任务
    asyncio.create_task(send_images())
    
    # 保持服务器运行
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())