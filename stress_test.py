import asyncio
import aiohttp
import time
from tqdm import tqdm

URL = "whatsapp-blur-detect.vercel.app"

async def post(image, session, progress_bar):
    time_start = time.time()
    async with session.post(URL, files={'image': image}) as response:
        progress_bar.update(1)
        await response
        time_end = time.time()
        return time_end - time_start

async def stress_test():
    with tqdm(total=17040) as progress_bar:
        with open('image.jpg', 'rb') as image:
            async with aiohttp.ClientSession() as session:
                tasks = [asyncio.create_task(coro=post(image, session, progress_bar)) for i in range(1, 10)]
                times = await asyncio.gather(*tasks, return_exceptions=False)
                print(f"Tasks        : {len(times)}")
                print(f"Tasks on-time: {sum([1 if t <= 3 else 0 for t in times])}")
                print(f"Total time   : {sum(times)}")
                print(f"Average time : {sum(times) / len(times)}")

asyncio.run(stress_test())