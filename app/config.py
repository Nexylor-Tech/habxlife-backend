from dotenv import load_dotenv
from pydantic import AnyUrl, SecretStr, field_validator 
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env") 
    SUPABASE_URL: AnyUrl
    SUPABASE_API_KEY: SecretStr
    SUPABASE_SERVICE_ROLE_KEY: SecretStr | None = None
    ALLOW_ORIGNINS: list[str] = ["*"]

    @field_validator("ALLOW_ORIGNINS", mode="before")
    def parse_allow_origins(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v
 
settings = Settings()