import asyncio
import logging
import os
from fastapi import FastAPI, HTTPException
import uvicorn
from semantic_search import *
from models import *
import requests
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

LOG = logging.getLogger(__name__)
LOG.info("API is starting up")
LOG.info(uvicorn.Config.asgi_version)


@app.post("/generate", response_model=GenerationResponse)
async def generate(user_input: GenerationRequest):
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    ENHANCER_ENDPOINT = os.getenv("ENHANCER_ENDPOINT")

    if not ENHANCER_ENDPOINT:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    # send the prompt to enhancer
    enhancer: EnhancerResponse = await (requests.post(ENHANCER_ENDPOINT, json={"prompt": prompt})).json()
    print(enhancer.enhanced_prompt)

    IMAGE_GENERATION_ENDPOINT = os.getenv("IMAGE_GENERATION_ENDPOINT")

    if not IMAGE_GENERATION_ENDPOINT:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    generated_image: ImageResponse = await (requests.post(IMAGE_GENERATION_ENDPOINT, json={"prompt": enhancer.enhanced_prompt})).json()

    return GenerationResponse(image_url=generated_image.image_url)


"""abstracted endpoints"""


@app.post("/send-to-enhancer", response_model=EnhancerResponse)
async def send_to_enhancer(user_input: EnhancerRequest):
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
@app.post("/send-to-img-gen", response_model=ImageResponse)
def send_to_img_gen(user_input: ImageRequest):
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    # call the image generation api here

    return ImageResponse(image_url="https://example.com/image.png")
