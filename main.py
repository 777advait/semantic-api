import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from semantic_search import *

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    keyword: str
    theme: str
    enhanced_prompt: str


@app.post("/enhance", response_model=PromptResponse)
async def enhance(user_input: PromptRequest):
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    keyword, theme = await asyncio.gather(extract_keyword(prompt), extract_description(prompt))

    if not keyword or not theme:
        raise HTTPException(
            status_code=500, detail="Failed to process the prompt")

    enhanced_prompt = await enhance_prompt(theme)

    return PromptResponse(
        keyword=keyword,
        theme=theme,
        enhanced_prompt=enhanced_prompt
    )
