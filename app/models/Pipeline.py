from pydantic import BaseModel


class PipelineRequest(BaseModel):
    prompt: str


class PipelineResponse(BaseModel):
    image_url: str
    mockup_url: str
