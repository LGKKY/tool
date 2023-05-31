import asyncio
import json
import os
import subprocess
from aiohttp import web

app = web.Application()

async def handle_webhook(request):
    # 即时返回http 200
    await asyncio.sleep(0)
    return web.Response()

async def process_webhook(data):
    json_data = json.loads(data)
    event_type = json_data.get("EventType")
    if event_type == "FileClosed":
        event_data = json_data.get("EventData")
        if event_data:
            relative_path = event_data.get("RelativePath")
            if relative_path:
                username = event_data.get("Name")
                # 执行命令
                cmd = f"OneDriveUploader -s rec/{relative_path} -r hime/{username}"
                subprocess.run(cmd, shell=True)
                # 等待命令执行完成后，移动文件
                await asyncio.sleep(0.1)
                old_path = f"rec/{relative_path}"
                new_path = f"rec/上传完成/{relative_path}"
                os.renames(old_path,new_path)

async def webhook(request):
    data = await request.text()
    asyncio.ensure_future(process_webhook(data))
    return web.Response()

app.add_routes([
    web.post('/webhook', webhook),
    web.get('/', handle_webhook),
])

if __name__ == '__main__':
    # 启动web服务
    web.run_app(app)


