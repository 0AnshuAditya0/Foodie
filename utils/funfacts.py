import os
import aiohttp
import random

async def get_food_fact():
    spoonacular_url = "https://api.spoonacular.com/food/trivia/random"
    spoonacular_key = os.getenv("SPOONACULAR_KEY")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(spoonacular_url, params={"apiKey": spoonacular_key}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["text"]
    except:
        pass  # fallback below

    # Fallback if API limit reached
    fallback_facts = [
        "Chocolate was once used as money.",
        "Apples float because they are 25% air.",
        "Bananas are berries, but strawberries are not.",
        "Potatoes were the first food grown in space.",
    ]
    return random.choice(fallback_facts)
