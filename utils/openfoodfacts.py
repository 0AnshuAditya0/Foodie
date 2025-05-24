import aiohttp

async def get_product_info(product_name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            try:
                product = data['products'][0]
                return f"**{product.get('product_name', 'No name')}**\nBrands: {product.get('brands', 'N/A')}\nCalories: {product.get('nutriments', {}).get('energy-kcal_100g', 'N/A')} kcal/100g"
            except IndexError:
                return "Product not found."
