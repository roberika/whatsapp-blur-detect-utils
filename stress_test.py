import asyncio
import aiohttp
import time
from tqdm.asyncio import tqdm

# kirim satu request
async def post(session: aiohttp.ClientSession):
    image = open('image.jpg', 'rb')
    time_start = time.time()
    async with session.post("https://whatsapp-blur-detect.vercel.app/stress-test", data=image) as response:
        await response.text()
        time_end = time.time()
        return time_end - time_start
async def bound_post(semaphore, session):
    async with semaphore:
        return await post(session)

# kirim n request secara async
async def stress_test(n):
    print(f"Running {n} times")
    semaphore = asyncio.Semaphore(1000)
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(n):
            task = asyncio.ensure_future(bound_post(semaphore, session))
            tasks.append(task)
            
        times = await tqdm.gather(*tasks)
        print(f"Tasks        : {len(times)}")
        print(f"Tasks on-time: {sum([1 if t <= 3 else 0 for t in times])}")
        print(f"Total time   : {sum(times)}")
        print(f"Max time     : {max(times)}")
        print(f"Average time : {sum(times) / len(times)}")

asyncio.run(stress_test(1))
asyncio.run(stress_test(2))
asyncio.run(stress_test(5))
asyncio.run(stress_test(10))
asyncio.run(stress_test(20))
asyncio.run(stress_test(50))
asyncio.run(stress_test(100))