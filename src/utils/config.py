from typing import Optional, List
from pydantic import BaseSettings, Field
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo-preview", env="OPENAI_MODEL")
    openai_temperature: float = Field(0.3, env="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(4000, env="OPENAI_MAX_TOKENS")
    
    # Alternative AI Models
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    google_api_key: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    
    # Vector Database Configuration
    vector_db_type: str = Field("faiss", env="VECTOR_DB_TYPE")
    vector_db_path: str = Field("./data/vector_store", env="VECTOR_DB_PATH")
    embedding_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    embedding_dimension: int = Field(384, env="EMBEDDING_DIMENSION")
    
    # Pinecone Configuration
    pinecone_api_key: Optional[str] = Field(None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(None, env="PINECONE_ENVIRONMENT")
    pinecone_index_name: Optional[str] = Field(None, env="PINECONE_INDEX_NAME")
    
    # Scraping Configuration
    max_concurrent_requests: int = Field(5, env="MAX_CONCURRENT_REQUESTS")
    request_delay: float = Field(1.0, env="REQUEST_DELAY")
    user_agent: str = Field(
        "AutonomousWebResearcher/1.0 (+https://github.com/your-username/autonomous-web-researcher)",
        env="USER_AGENT"
    )
    respect_robots_txt: bool = Field(True, env="RESPECT_ROBOTS_TXT")
    max_page_size: int = Field(10485760, env="MAX_PAGE_SIZE")  # 10MB
    
    # Browser Configuration
    headless_browser: bool = Field(True, env="HEADLESS_BROWSER")
    browser_timeout: int = Field(30000, env="BROWSER_TIMEOUT")  # 30 seconds
    viewport_width: int = Field(1280, env="VIEWPORT_WIDTH")
    viewport_height: int = Field(720, env="VIEWPORT_HEIGHT")
    
    # Content Processing
    max_chunk_size: int = Field(1000, env="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    min_content_length: int = Field(100, env="MIN_CONTENT_LENGTH")
    max_content_length: int = Field(100000, env="MAX_CONTENT_LENGTH")
    
    # API Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    api_workers: int = Field(1, env="API_WORKERS")
    debug_mode: bool = Field(False, env="DEBUG_MODE")
    
    # Search and Retrieval
    max_search_results: int = Field(10, env="MAX_SEARCH_RESULTS")
    similarity_threshold: float = Field(0.7, env="SIMILARITY_THRESHOLD")
    confidence_threshold: float = Field(0.6, env="CONFIDENCE_THRESHOLD")
    
    # Caching
    enable_cache: bool = Field(True, env="ENABLE_CACHE")
    cache_ttl: int = Field(3600, env="CACHE_TTL")  # 1 hour
    cache_path: str = Field("./data/cache", env="CACHE_PATH")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("./logs/autonomous_web_researcher.log", env="LOG_FILE")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Security
    allowed_domains: str = Field("", env="ALLOWED_DOMAINS")  # Comma-separated
    blocked_domains: str = Field(
        "localhost,127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16",
        env="BLOCKED_DOMAINS"
    )
    max_redirects: int = Field(5, env="MAX_REDIRECTS")
    verify_ssl: bool = Field(True, env="VERIFY_SSL")
    
    # Rate Limiting
    requests_per_minute: int = Field(60, env="REQUESTS_PER_MINUTE")
    requests_per_hour: int = Field(1000, env="REQUESTS_PER_HOUR")
    
    # Database
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    database_echo: bool = Field(False, env="DATABASE_ECHO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def allowed_domains_list(self) -> List[str]:
        """Get allowed domains as a list."""
        if not self.allowed_domains:
            return []
        return [domain.strip() for domain in self.allowed_domains.split(",") if domain.strip()]

    @property
    def blocked_domains_list(self) -> List[str]:
        """Get blocked domains as a list."""
        return [domain.strip() for domain in self.blocked_domains.split(",") if domain.strip()]

    def create_directories(self):
        """Create necessary directories if they don't exist."""
        dirs_to_create = [
            Path(self.vector_db_path).parent,
            Path(self.cache_path),
            Path(self.log_file).parent,
        ]
        
        if self.database_url and self.database_url.startswith("sqlite"):
            # Extract directory from SQLite URL
            db_path = self.database_url.replace("sqlite:///", "")
            dirs_to_create.append(Path(db_path).parent)
        
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Create necessary directories on import
settings.create_directories()