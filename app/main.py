import asyncio
from fastapi import FastAPI
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

URLS_ENV = os.getenv('URLS')

URLS = URLS_ENV.split(',')
URLS = [url.strip() for url in URLS]

async def keep_running():
    while True:
        async with httpx.AsyncClient() as client:
            for url in URLS:
                await client.get(url)
        await asyncio.sleep(10)

@app.get('/')
async def read_root():
    return {'hello': 'world'}

@app.get('/trigger')
async def run_trigger():
    coro = keep_running()
    asyncio.create_task(coro)
    return {'message': 'trigger successful'}

@app.get('/health')
async def health_check():
    return {'status': 'ok'}
