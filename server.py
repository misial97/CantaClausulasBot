# Copyright (c) 2025 Miguel Sierra
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

import os, asyncio, signal
from fastapi import FastAPI
from dotenv import load_dotenv
from logger import logger
from main import run_once

app = FastAPI()
load_dotenv()

RUN_INTERVAL_SEC = int(os.getenv("RUN_INTERVAL_SEC", "30"))
_running = True

@app.head("/health")
def health():
    return {"ok": True}

@app.get("/health")
def health():
    return {"ok": True}

async def worker_loop():
    global _running
    while _running:
        try:
            await asyncio.to_thread(run_once)
        except Exception as e:
            logger.info("Worker error:", e)
        await asyncio.sleep(RUN_INTERVAL_SEC)

@app.on_event("startup")
async def on_start():
    asyncio.create_task(worker_loop())

def _graceful(*_):
    global _running
    _running = False

signal.signal(signal.SIGTERM, _graceful)
signal.signal(signal.SIGINT, _graceful)