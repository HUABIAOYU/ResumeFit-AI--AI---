from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    app_name: str = "ResumeFit AI"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"]

    log_dir: str = "./logs"
    log_level: str = "INFO"
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB 单文件上限
    log_backup_count: int = 5               # 保留最近 5 个备份

    database_url: str = "postgresql+asyncpg://user_YXFpcX:password_HWa7G7@127.0.0.1:5432/resumefit"

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    pdf_max_size_mb: int = 5
    resume_min_chars: int = 100

    upload_dir: str = "./uploads"


settings = Settings()
