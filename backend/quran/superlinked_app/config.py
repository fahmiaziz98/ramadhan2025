import os
from dotenv import load_dotenv, find_dotenv
from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

load_dotenv(find_dotenv())

class Settings(BaseSettings):

    EMBEDDING_MODEL: Literal["intfloat/multilingual-e5-small"] = "intfloat/multilingual-e5-small"  
    ARABIC_EMBEDDING_MODEL: Literal["sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"] = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  

    # use qdrant
    dataset_type: Literal["hadist", "quran"] = "hadist"  # Add dataset_type parameter
    USE_QDRANT : bool = False  # Set default to False
    QDRANT_URL_BASE: str | None = os.getenv("QDRANT_URL_BASE")
    QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY")


    @model_validator(mode="after")
    def check_qdrant_connection(self):
        # Set USE_QDRANT based on dataset_type
        self.USE_QDRANT = self.dataset_type == "hadist"  
        
        if self.USE_QDRANT:
            required_settings = {
                "QDRANT_URL_BASE": self.QDRANT_URL_BASE,
                "QDRANT_API_KEY": self.QDRANT_API_KEY,
            }
            for name, value in required_settings.items():
                if not value:
                    raise ValueError(f"{name} is required when USE_QDRANT is True")
        return self


settings = Settings(dataset_type="quran")  # USE_QDRANT akan otomatis False