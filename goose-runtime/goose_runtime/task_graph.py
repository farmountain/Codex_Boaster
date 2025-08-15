from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


@dataclass
class Task:
    """A unit of work in the task graph."""

    name: str
    coro: Callable[[Dict[str, Any]], Awaitable[Any]]
    deps: List[str] = field(default_factory=list)
    retries: int = 0
    result: Any = None

    async def run(self, context: Dict[str, Any]) -> Any:
        attempt = 0
        while True:
            try:
                with tracer.start_as_current_span("thought") as span:
                    span.set_attribute("task.name", self.name)
                    self.result = await self.coro(context)
                with tracer.start_as_current_span("output") as span:
                    span.set_attribute("task.name", self.name)
                    span.set_attribute("task.result", str(self.result))
                return self.result
            except Exception as exc:  # pragma: no cover - retry logic
                attempt += 1
                if attempt > self.retries:
                    with tracer.start_as_current_span("output") as span:
                        span.set_attribute("task.name", self.name)
                        span.record_exception(exc)
                    raise
                await asyncio.sleep(0)


class TaskGraph:
    """Execute tasks respecting their dependencies with parallelism."""

    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}
        self._cache: Dict[str, asyncio.Task] = {}

    def add_task(self, task: Task) -> None:
        self.tasks[task.name] = task

    async def _run_task(
        self, name: str, semaphore: asyncio.Semaphore, context: Dict[str, Any]
    ) -> Any:
        if name in self._cache:
            return await self._cache[name]
        task = self.tasks[name]

        async def runner() -> Any:
            for dep in task.deps:
                await self._run_task(dep, semaphore, context)
            async with semaphore:
                return await task.run(context)

        self._cache[name] = asyncio.create_task(runner())
        return await self._cache[name]

    async def run(
        self, max_concurrency: int = 5, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run all tasks in the graph and return their results."""

        semaphore = asyncio.Semaphore(max_concurrency)
        context = context or {}
        await asyncio.gather(
            *(self._run_task(name, semaphore, context) for name in self.tasks)
        )
        return {name: t.result for name, t in self.tasks.items()}
