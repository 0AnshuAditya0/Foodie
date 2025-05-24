import aiohttp
from discord.ext import commands
import discord

async def get_recipe_by_name(ctx, name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            meals = data.get("meals")
            if not meals:
                await ctx.send("🚫 No recipe found for that name.")
                return

            meal = meals[0]
            embed = discord.Embed(
                title=f"🍽️ {meal['strMeal']}",
                description=f"**Category:** {meal['strCategory']}\n**Area:** {meal['strArea']}",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=meal["strMealThumb"])
            embed.add_field(name="📝 Instructions", value=meal["strInstructions"][:500] + "...", inline=False)
            embed.add_field(name="🎥 Watch / Source", value=meal["strSource"] or meal["strYoutube"] or "Not available", inline=False)
            await ctx.send(embed=embed)



async def get_random_meal(ctx):
    print("randommeal command triggered")
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            meal = data["meals"][0]

            embed = discord.Embed(
                title=f"🎲 Random Recipe: {meal['strMeal']}",
                description=f"**Category:** {meal['strCategory']}\n**Area:** {meal['strArea']}",
                color=discord.Color.blurple()
            )
            embed.set_thumbnail(url=meal["strMealThumb"])
            embed.add_field(
                name="📝 Instructions", 
                value=(meal["strInstructions"][:500] + "...") if len(meal["strInstructions"]) > 500 else meal["strInstructions"],
                inline=False
            )
            embed.add_field(
                name="🎥 Watch / Source", 
                value=meal["strSource"] or meal["strYoutube"] or "Not available",
                inline=False
            )
            await ctx.send(embed=embed)



async def get_meals_by_area(area):
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={area}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data.get("meals")