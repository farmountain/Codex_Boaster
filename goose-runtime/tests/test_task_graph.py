import asyncio
import sys
import time
from pathlib import Path

# Ensure package path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from goose_runtime import Task, TaskGraph


def test_parallel_execution():
    start = time.perf_counter()

    async def a(_):
        await asyncio.sleep(0.1)
        return "a"

    async def b(_):
        await asyncio.sleep(0.1)
        return "b"

    tg = TaskGraph()
    tg.add_task(Task("a", a))
    tg.add_task(Task("b", b))
    results = asyncio.run(tg.run(max_concurrency=2))
    elapsed = time.perf_counter() - start
    assert results == {"a": "a", "b": "b"}
    assert elapsed < 0.2  # parallel execution


def test_retry():
    attempts = {"count": 0}

    async def flaky(_):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("fail")
        return "ok"

    tg = TaskGraph()
    tg.add_task(Task("t", flaky, retries=2))
    results = asyncio.run(tg.run())
    assert results == {"t": "ok"}
    assert attempts["count"] == 3
