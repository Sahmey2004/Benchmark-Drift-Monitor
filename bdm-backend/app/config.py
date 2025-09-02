
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(default="sqlite+aiosqlite:///./bdm.db", alias="BDM_DATABASE_URL")
    td_threshold_bps: int = Field(default=30, alias="BDM_TD_THRESHOLD_BPS")
    te_window_days: int = Field(default=30, alias="BDM_TE_WINDOW_DAYS")
    te_threshold_bps: int = Field(default=50, alias="BDM_TE_THRESHOLD_BPS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
