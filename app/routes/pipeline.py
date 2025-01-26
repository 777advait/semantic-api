from fastapi import APIRouter

from app.controllers.pipeline import PipelineController
from app.models.Pipeline import PipelineRequest, PipelineResponse


router = APIRouter()


@router.post("/generate", response_model=PipelineResponse)
async def run_pipeline(user_input: PipelineRequest):
    return await PipelineController.run_pipeline(user_input)
