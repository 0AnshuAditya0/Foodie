import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import re
import asyncio
import aiohttp
import random
import pycountry

from utils.scoreboard import update_score, get_user_score, get_leaderboard


from utils.foodish import get_random_food_image
from utils.themealdb import get_recipe_by_name, get_random_meal, get_meals_by_area
from utils.openfoodfacts import get_product_info
from utils.funfacts import get_food_fact



load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="O", intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="🍳 Cooking up some commands"))
    print(f"Logged in as {bot.user} 💘")

@bot.command()
async def hellofoodie(ctx):
    embed = discord.Embed(
        title="Hey foodie! 👋",
        description="I'm your cute little Food Bot here to spice things up 🌶️",
        color=0xFFC0CB
    )
    embed.set_footer(text="Type !help to see my tasty tricks 😋")
    await ctx.send(embed=embed)






@bot.command()
async def foodpic(ctx):
    url = await get_random_food_image()
    await ctx.send(url)

@bot.command()
async def recipe(ctx, *, name):
    result = await get_recipe_by_name(name)
    await ctx.send(result)

@bot.command()
async def randommeal(ctx):
    result = await get_random_meal()
    await ctx.send(result)

@bot.command()
async def product(ctx, *, name):
    result = await get_product_info(name)
    await ctx.send(result)



@bot.command()
async def guessfood(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://foodish-api.com/api/") as resp:
            data = await resp.json()
            url = data["image"]
           
            match = re.search(r'/images/([^/]+)/', url)
            if match:
                answer = match.group(1).replace('-', ' ').lower()
            else:
                answer = "unknown food"

    embed = discord.Embed(title="🍲 Guess the Dish!", description="Type your guess in 20 seconds!", color=0xffc107)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=20.0, check=check)
        guess = msg.content.lower()

        answer_words = set(answer.split())
        guess_words = set(guess.split())

        if answer == "unknown food":
            await ctx.send("I couldn't figure it out either! 😅 No points this round.")
        elif answer in guess or guess in answer:
            update_score(ctx.author.id, ctx.author.name)
            await ctx.send(f"🎉 Spot on! It was **{answer.title()}**!")
        elif answer_words & guess_words:
            await ctx.send(f"😮 Close guess! You said something right, but the full dish was **{answer.title()}**.")
        else:
            await ctx.send(f"❌ Nope! The correct answer was **{answer.title()}**.")
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ Time's up! The correct answer was **{answer.title()}**.")



@bot.command()
async def myscore(ctx):
    score = get_user_score(ctx.author.id)
    await ctx.send(f"🍽️ {ctx.author.name}, your score is **{score}**!")

@bot.command()
async def leaderboard(ctx):
    top_players = get_leaderboard()
    msg = "**🥇 Foodie Leaderboard 🥇**\n"
    for i, (user_id, data) in enumerate(top_players, start=1):
        msg += f"{i}. {data['username']} — {data['score']} points\n"
    await ctx.send(msg)



@bot.command()
async def foodfact(ctx):
    await ctx.typing()  
    await asyncio.sleep(2)  
    fact = await get_food_fact()
    embed = discord.Embed(title="🍽️ Random Food Fact", description=fact, color=0xFFA07A)
    await ctx.send(embed=embed)


@bot.command()
async def sweetness(ctx):
    await ctx.typing()
    await asyncio.sleep(2)

    percent = random.randint(50, 100)
    desserts = [
        "chocolate fudge brownie 🍫", "strawberry shortcake 🍓",
        "raspberry macaron 🍥", "cotton candy cloud 🍭",
        "vanilla cupcake with rainbow sprinkles 🧁", "gulab jamun 🍮"
    ]
    dessert = random.choice(desserts)

    embed = discord.Embed(
        title="💖 Sweetness Meter",
        description=f"You're **{percent}% sweet**, just like a {dessert}",
        color=0xFFC0CB
    )
    await ctx.send(embed=embed)



@bot.command()
async def foodtherapy(ctx):
    await ctx.typing()
    await asyncio.sleep(2)

    quotes = [
        "You are doing better than you think. 🌸",
        "Even the tiniest step forward is progress. 🌿",
        "Take a deep breath, you’ve got this. 🌈",
        "Rest is productive too. ☁️",
        "Kindness to yourself is never wasted. 🌷"
    ]

    comfort_foods = [
        "hot bowl of ramen 🍜", "buttery mashed potatoes 🥔",
        "warm chocolate chip cookies 🍪", "a soft pancake stack 🥞",
        "fluffy rice with ghee and dal 🍚", "creamy mac & cheese 🧀"
    ]

    quote = random.choice(quotes)
    food = random.choice(comfort_foods)

    embed = discord.Embed(
        title="🧘‍♀️ Food Therapy Session",
        description=f"{quote}\n\nHere, have a {food} and relax 💖",
        color=0xADD8E6
    )
    await ctx.send(embed=embed)




def country_to_flag(country_name):
    try:
        country = pycountry.countries.lookup(country_name.strip())
        country_code = country.alpha_2.upper()

        flag = chr(127397 + ord(country_code[0])) + chr(127397 + ord(country_code[1]))
        return flag
    except LookupError:
        return "🌍"
    


@bot.command()
async def countrydish(ctx, *, country: str):
    flag = country_to_flag(country)
    meals = await get_meals_by_area(country)

    if not meals:
        await ctx.send(f"Sorry love, I couldn't find any dishes for **{country}** 😞")
        return

    sample_meals = meals[:3]  # pick top 3
    embed = discord.Embed(
        title=f"{flag} {country.title()} Cuisine",
        description=f"Here are some famous dishes from **{country.title()}** 🍽️",
        color=discord.Color.orange()
    )

    for meal in sample_meals:
        embed.add_field(name=meal['strMeal'], value='Yumm ✨', inline=False)

    embed.set_thumbnail(url=sample_meals[0].get("strMealThumb", ""))

    await ctx.send(embed=embed)


async def get_random_meal():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.themealdb.com/api/json/v1/1/random.php") as resp:
            data = await resp.json()
            meal = data["meals"][0]
            return {
                "name": meal["strMeal"],
                "category": meal["strCategory"],
                "area": meal["strArea"],
                "image": meal["strMealThumb"],
                "youtube": meal["strYoutube"],
                "instructions": meal["strInstructions"]
            }

@bot.command()
async def sendmeal(ctx, member: discord.Member):
    meal = await get_random_meal()

    embed = discord.Embed(
        title=f"🍽️ {ctx.author.display_name} just sent a meal to {member.display_name}!",
        description=f"**{meal['name']}** ({meal['area']} - {meal['category']})\n\n**Instructions:** {meal['instructions'][:200]}...",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url=meal['image'])
    embed.add_field(name="🎥 YouTube", value=meal['youtube'], inline=False)
    embed.set_footer(text="Made with love and food 💖")

    await ctx.send(content=f"{member.mention}", embed=embed)



@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🍽️ Foodie Bot Help Menu",
        description="Hey sweetheart, here's everything your personal food bot can do! 💕\nUse these commands to make every meal fun!",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="👋 `!hellofoodie`",
        value="Greet your bot foodie-style.\n**Example:** `!hellofoodie`",
        inline=False
    )

    embed.add_field(
        name="🍜 `!randommeal`",
        value="Get a surprise random meal.\n**Example:** `!randommeal`",
        inline=False
    )

    embed.add_field(
        name="📸 `!foodpic`",
        value="Get a random food picture (cute and aesthetic!)\n**Example:** `!foodpic`",
        inline=False
    )

    embed.add_field(
        name="📚 `!foodfact`",
        value="Learn a fun and random food fact.\n**Example:** `!foodfact`",
        inline=False
    )

    embed.add_field(
        name="🌍 `!countrydish <country>`",
        value="Get a famous dish from a specific country.\n**Example:** `!countrydish japanese`",
        inline=False
    )

    embed.add_field(
        name="🧠 `!foodtherapy`",
        value="Feeling down? Let me cheer you up with kind words and food vibes 🍰\n**Example:** `!foodtherapy`",
        inline=False
    )

    embed.add_field(
        name="🧩 `!guessfood`",
        value="Play a food guessing game with emojis!\n**Example:** `!guessfood`",
        inline=False
    )

    embed.add_field(
        name="🥄 `!recipe <meal>`",
        value="Get a recipe for a meal you want to make.\n**Example:** `!recipe Pasta`",
        inline=False
    )

    embed.add_field(
        name="📦 `!product <food>`",
        value="Search real food products from OpenFoodFacts.\n**Example:** `!product Nutella`",
        inline=False
    )

    embed.add_field(
        name="🍭 `!sweetness`",
        value="Get a random sweet dish suggestion (dessert lover’s heaven!)\n**Example:** `!sweetness`",
        inline=False
    )

    embed.add_field(
        name="🎯 `!sendmeal @user`",
        value="Send a surprise meal to someone in the server ❤️\n**Example:** `!sendmeal @babe`",
        inline=False
    )

    embed.add_field(
        name="🏆 `!leaderboard`",
        value="See who’s the top foodie in the server (based on sent/received meals)!\n**Example:** `!leaderboard`",
        inline=False
    )

    embed.add_field(
        name="📊 `!myscore`",
        value="Check your personal foodie stats.\n**Example:** `!myscore`",
        inline=False
    )


    embed.set_footer(text="Bon appétit! Type any command to get started 🍴")
    await ctx.send(embed=embed)



bot.run(TOKEN)
