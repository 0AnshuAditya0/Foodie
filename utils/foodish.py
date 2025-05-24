import aiohttp

async def get_random_food_image():
    url = "https://foodish-api.com/api/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["image"]
            else:
                return "⚠️ Couldn't fetch food image 😢"
