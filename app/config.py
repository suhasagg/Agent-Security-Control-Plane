from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url:str="postgresql+asyncpg://postgres:postgres@localhost:5432/security"
    api_key:str="change-me"
    policy_version:str="2026-10-04"
    approval_ttl_seconds:int=900
    max_delegation_depth:int=4
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
