import os

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://owpublic.blob.core.windows.net/tech-task")

config: Config = Config()
