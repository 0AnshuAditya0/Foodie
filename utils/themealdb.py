import aiohttp

async def get_recipe_by_name(name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            meals = data.get("meals")
            if not meals:
                return "No recipe found."
            meal = meals[0]
            return f"**{meal['strMeal']}**\nCategory: {meal['strCategory']}\nRecipe: {meal['strInstructions'][:300]}...\nMore: {meal['strSource'] or meal['strYoutube']}"

async def get_random_meal():
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            meal = data['meals'][0]
            return f"**{meal['strMeal']}**\nCategory: {meal['strCategory']}\nRecipe: {meal['strInstructions'][:300]}...\nMore: {meal['strSource'] or meal['strYoutube']}"

async def get_meals_by_area(area):
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={area}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data.get("meals")