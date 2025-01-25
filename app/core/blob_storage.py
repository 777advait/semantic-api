from azure.storage.blob import BlobServiceClient, ContentSettings
from app.core.config import settings


class BlobStorage:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING)

    def upload_generated_image(self, blob_name: str, data: bytes) -> str:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=settings.GENERATED_IMAGES_CONTAINER_NAME, blob=blob_name)

            blob_client.upload_blob(
                data, content_settings=ContentSettings(content_type="image/png"))

            print(
                f"Blob {blob_name} uploaded to container {
                    settings.GENERATED_IMAGES_CONTAINER_NAME}"
            )

            return blob_client.url

        except Exception as e:
            print(f"Error uploading blob: {e}")
            return None


blob_storage = BlobStorage()
