from pydantic import BaseModel


class ImageGenerationRequest(BaseModel):
    prompt: str


class ImageGenerationResponse(BaseModel):
    image_url: str
