import asyncio
from fastapi import APIRouter, HTTPException

from app.models.ImageGeneration import ImageGenerationRequest
from app.models.Pipeline import PipelineRequest, PipelineResponse
from app.services.image_generation import generate_image
from app.services.semantic_search import enhance_prompt, extract_description, extract_keyword


router = APIRouter()

@router.post("/generate", response_model=PipelineResponse)
async def run_pipeline(user_input: PipelineRequest):
    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")
    
    keyword, theme = await asyncio.gather(extract_keyword(prompt), extract_description(prompt))

    if not keyword or not theme:
        raise HTTPException(
            status_code=500, detail="Failed to process the prompt")
    
    enhanced_prompt = await enhance_prompt(theme)

    image = generate_image(ImageGenerationRequest(prompt=enhanced_prompt))

    return PipelineResponse(
        image_url=image.image_url,
        mockup_url=image.image_url
    )
