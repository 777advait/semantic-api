from datetime import datetime
import uuid
from fastapi import HTTPException
import requests
from app.core.blob_storage import blob_storage
from app.models.ImageGeneration import ImageGenerationRequest, ImageGenerationResponse
from app.core.config import settings


def generate_unique_filename(extension='png'):
    unique_id = uuid.uuid4()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"image_{timestamp}_{unique_id}.{extension}"


def generate_image(user_input: ImageGenerationRequest):

    prompt = user_input.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Please enter a prompt")

    # Replace with your token
    headers = {"Authorization": f"Bearer {settings.HF_ACCESS_TOKEN}"}

    try:
        # Call Hugging Face API
        response = requests.post(
            settings.HF_API_ENDPOINT, headers=headers, json={"inputs": prompt})

        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail=f"Error from Hugging Face API: {response.text}")

        # Return image as bytes or URL (adapt storage as needed)
        # image_path = f"generated_images/{prompt.replace(' ', '_')}.png"
        # with open(image_path, "wb") as f:
        #     f.write(response.content)

        # return ImageGenerationResponse(image_url=f"http://localhost:8000/{image_path}")

        image_url = blob_storage.upload_generated_image(
            blob_name=generate_unique_filename(), data=response.content)

        return ImageGenerationResponse(image_url=image_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
