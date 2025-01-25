from pydantic import BaseModel


class EnhancerRequest(BaseModel):
    prompt: str


class EnhancerResponse(BaseModel):
    keyword: str
    theme: str
    enhanced_prompt: str


class ImageRequest(BaseModel):
    prompt: str


class ImageResponse(BaseModel):
    image_url: str


class GenerationRequest(BaseModel):
    prompt: str


class GenerationResponse(BaseModel):
    image_url: str
