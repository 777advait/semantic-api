import asyncio
import os
from fastapi import FastAPI, HTTPException
from semantic_search import *
from models import *
import requests
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()


@app.post("/generate", response_model=GenerationResponse)
async def generate(user_input: GenerationRequest):
    print("inside generate")
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    ENHANCER_ENDPOINT = os.getenv("ENHANCER_ENDPOINT")

    if not ENHANCER_ENDPOINT:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    # send the prompt to enhancer
    enhancer: EnhancerResponse = await send_to_enhancer(
        EnhancerRequest(prompt=prompt))
    print(enhancer.enhanced_prompt)

    IMAGE_GENERATION_ENDPOINT = os.getenv("IMAGE_GENERATION_ENDPOINT")

    if not IMAGE_GENERATION_ENDPOINT:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    generated_image: ImageResponse = await send_to_img_gen(
        ImageRequest(prompt=enhancer.enhanced_prompt))

    return GenerationResponse(image_url=generated_image.image_url)


"""abstracted endpoints"""


# @app.post("/send-to-enhancer", response_model=EnhancerResponse)
async def send_to_enhancer(user_input: EnhancerRequest):
    print("inside send_to_enhancer")
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    keyword, theme = await asyncio.gather(extract_keyword(prompt), extract_description(prompt))

    if not keyword or not theme:
        raise HTTPException(
            status_code=500, detail="Failed to process the prompt")

    enhanced_prompt = await enhance_prompt(theme)

    return EnhancerResponse(
        keyword=keyword,
        theme=theme,
        enhanced_prompt=enhanced_prompt
    )


# dummy endpoint, image generation api should be separate
# @app.post("/send-to-img-gen", response_model=ImageResponse)
async def send_to_img_gen(user_input: ImageRequest):
    print("inside send_to_img_gen")
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    # call the image generation api here

    return ImageResponse(image_url="https://example.com/image.png")
