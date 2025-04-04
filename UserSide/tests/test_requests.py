import asyncio
import aiohttp
import time

URL = "https://qrmenuarmenia.site/api/api/menu-filter/all-menu/1"
NUM_REQUESTS = 1250  # approximatly 5 requests at the same time of each user
CONCURRENT_REQUESTS = 250  # Control the number of simultaneous connections approximtly 4-5 cafes, each cafe 50 user at the same time

async def fetch(session, request_id):
    try:
        async with session.get(URL, timeout=10) as response:
            status = response.status
            text = await response.text()
            return f"Request {request_id}: Status {status}"
    except Exception as e:
        return f"Request {request_id}: Failed ({str(e)})"

async def main():
    start_time = time.time()

    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)  # Manage concurrency
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, i) for i in range(1, NUM_REQUESTS + 1)]
        results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

    elapsed_time = time.time() - start_time
    print(f"\nCompleted {NUM_REQUESTS} requests in {elapsed_time:.2f} seconds.")

# Run the async event loop
asyncio.run(main())

