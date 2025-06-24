from pydantic import BaseModel, Field, SecretStr, SerializationInfo, field_serializer
from pydantic.json import pydantic_encoder

class MediaConfig(BaseModel):
    """Configuration for media generation tools.
    
    Attributes:
        gcp_project_id: The Google Cloud Project ID for Vertex AI.
        gcp_location: The Google Cloud location/region for Vertex AI.
        gcs_output_bucket: The GCS bucket URI for storing temporary media files.
    """
    gcp_project_id: str | None = Field(default=None, description="Google Cloud Project ID for Vertex AI")
    gcp_location: str | None = Field(default=None, description="Google Cloud location/region for Vertex AI") 
    gcs_output_bucket: str | None = Field(default=None, description="GCS bucket URI for storing temporary media files (e.g., gs://my-bucket-name)") 
    google_ai_studio_api_key: SecretStr | None = Field(default=None, description="Google AI Studio API key")

    @field_serializer('google_ai_studio_api_key')
    def api_key_serializer(self, api_key: SecretStr | None, info: SerializationInfo):
        """Custom serializer for API keys.

        To serialize the API key instead of ********, set expose_secrets to True in the serialization context.
        """
        if api_key is None:
            return None

        context = info.context
        if context and context.get('expose_secrets', False):
            return api_key.get_secret_value()

        return pydantic_encoder(api_key)
