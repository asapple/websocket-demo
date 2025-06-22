import asyncio
import websockets
import os
import time
from datetime import datetime

# 图片保存目录
SAVE_DIR = "./received_images"
os.makedirs(SAVE_DIR, exist_ok=True)

async def receive_images():
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        print("已连接到服务器，等待接收图片...")
        
        # 持续接收服务器发送的消息
        async for message in websocket:
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"
            save_path = os.path.join(SAVE_DIR, filename)
            
            # 保存接收到的图片
            with open(save_path, "wb") as f:
                f.write(message)
            print(f"图片已保存: {filename}")

if __name__ == "__main__":
    asyncio.run(receive_images())