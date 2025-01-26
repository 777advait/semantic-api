import requests
from app.models.ImageGeneration import ImageGenerationRequest
from app.models.Pipeline import PipelineRequest, PipelineResponse
from app.services.image_generation import generate_image
from app.services.semantic_search import enhance_prompt, extract_description, extract_keyword
import asyncio
from fastapi import HTTPException


class PipelineController:
    @staticmethod
    async def run_pipeline(user_input: PipelineRequest) -> PipelineResponse:
        try:
            prompt = user_input.prompt.strip()

            if not prompt:
                raise HTTPException(
                    status_code=400, detail="Please enter a prompt")

            keyword, theme = await asyncio.gather(extract_keyword(prompt), extract_description(prompt))

            if not keyword or not theme:
                raise HTTPException(
                    status_code=500, detail="Failed to process the prompt")

            enhanced_prompt = await enhance_prompt(theme)

            image = generate_image(
                ImageGenerationRequest(prompt=enhanced_prompt))

            return PipelineResponse(
                image_url=image.image_url
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to process the prompt: {e}")
