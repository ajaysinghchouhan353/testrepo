import asyncio
from collections.abc import Awaitable, Callable
from omas.models import GenerationJob


WorkerFn = Callable[[GenerationJob], Awaitable[None]]


class GenerationQueue:
    def __init__(self, workers: int, retry_count: int) -> None:
        self._queue: asyncio.Queue[GenerationJob | None] = asyncio.Queue()
        self._workers = workers
        self._retry_count = retry_count
        self.completed = 0
        self.failed = 0

    async def put(self, job: GenerationJob) -> None:
        await self._queue.put(job)

    async def run(self, worker_fn: WorkerFn) -> None:
        async def worker() -> None:
            while True:
                job = await self._queue.get()
                if job is None:
                    self._queue.task_done()
                    break
                try:
                    await worker_fn(job)
                    self.completed += 1
                except Exception as exc:  # noqa: BLE001
                    if job.retries < self._retry_count:
                        job.retries += 1
                        job.error = str(exc)
                        await self._queue.put(job)
                    else:
                        self.failed += 1
                        job.error = str(exc)
                finally:
                    self._queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(self._workers)]
        await self._queue.join()
        for _ in workers:
            await self._queue.put(None)
        await asyncio.gather(*workers)
