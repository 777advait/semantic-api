import ollama
from datetime import datetime


chosen_model = 'artifish/llama3.2-uncensored:latest'


async def extract_keyword(_prompt_: str) -> str:

    try:
        start = datetime.now()
        response = ollama.generate(
            model=chosen_model,
            prompt=f"Identify the product/item in {_prompt_}. For example, in the phrase Batman Coffee Mug, you have to identify Coffee Mug as the product/item. Respond with just the product name (like in my case, you just have to output Coffee Mug) and nothing else. A few examples of product types are as follows: 1. T-Shirts 2. Hoodies 3. Sweatshirts 4. Tank Tops 5. Crop tops 6. Crop hoodie 7. Maternity dresses 8. Caps 9. Long Sleeve Shirts 10. Polo Shirts 11. Dresses 12. Skirts 13. Leggings 14. Scarves 15. Bandanas 16. Aprons 17. Phone Cases 18. Laptop Sleeves 19. Tablet Sleeves 20. Mugs 21. Water Bottles 22. Tote Bags 23. Backpacks 24. Drawstring Bags 25. Beach Towels 26. Blankets 27. Pillows 28. Posters 29. Stickers 30. Buttons 31. Magnets 32. Keychains 33. Pin Badges 34. Pet Accessories (such as pet tags, pet bowls, and pet bandanas) 35. Home Decor (such as wall art, throw pillows, and blankets) 36. Accessories (such as hats, socks, and jewelry) 37. Stationery (such as notebooks, journals, and greeting cards) 38. Pet Beds 39. Shorts 40. Joggers ",
        )
        duration = datetime.now() - start
        keyword = response.get('response', '').strip()
        print("Keyword: ", keyword, f" ({duration.total_seconds():.2f} s)")
        return keyword if keyword else None

    except Exception as e:
        print(f"Error extracting keyword/theme: {e}")
        return None


async def extract_description(_prompt_: str) -> str:

    try:
        start = datetime.now()
        response = ollama.generate(
            model=chosen_model,
            prompt=f"Identify the theme/description in {
                _prompt_}. For example, in the phrase Batman Coffee Mug, you have to identify Batman as the theme/description. Respond with just the description/theme (like in my case, you just have to output Batman) and nothing else",
        )
        duration = datetime.now() - start
        description = response.get('response', '').strip()
        print("Description: ",  description,
              f" ({duration.total_seconds():.2f} s)")

        return description if description else None

    except Exception as e:
        print(f"Error extracting keyword/theme: {e}")
        return None


async def enhance_prompt(_theme_: str) -> str:

    try:
        start = datetime.now()
        response = ollama.generate(
            model=chosen_model,
            prompt=f"Enhance the following prompt: {
                _theme_} to make it suitable for image generation. Only output the enhanced prompt and nothing else",
        )
        duration = datetime.now() - start
        print(f"Prompt enhancement took {
              duration.total_seconds():.2f} seconds")
        enhance = response.get('response', '').strip()
        print("Enhanced prompt: ", enhance,
              f" ({duration.total_seconds():.2f} s)")

        return enhance if enhance else None

    except Exception as e:
        print(f"Error extracting keyword/theme: {e}")
        return None
