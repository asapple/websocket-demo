import asyncio
import websockets
import os
import time
from datetime import datetime
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='WebSocket Image Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8765, help='Server port')
    parser.add_argument('--dir', type=str, default='./received_images', help='Save directory')
    return parser.parse_args()

async def receive_images():
    args = parse_args()
    
    # 确保保存目录存在
    os.makedirs(args.dir, exist_ok=True)
    
    uri = f"ws://{args.host}:{args.port}"
    print(f"连接到服务器: {uri}")
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("连接成功，等待接收图片...")
                
                # 持续接收服务器发送的消息
                async for message in websocket:
                    # 生成带时间戳的文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filename = f"image_{timestamp}.jpg"
                    save_path = os.path.join(args.dir, filename)
                    
                    # 保存接收到的图片
                    with open(save_path, "wb") as f:
                        f.write(message)
                    print(f"图片已保存: {filename} ({len(message)} 字节)")
                    
        except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError) as e:
            print(f"连接断开: {e}")
            print("尝试在5秒后重新连接...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(receive_images())