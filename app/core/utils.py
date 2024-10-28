import aiohttp

async def fetch_client(url: str):
    headers = {
        "User-Agent": "fastapi",
        "Accept": "application/json",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None
