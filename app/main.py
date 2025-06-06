import logging.config
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.v1 import user, auth, crop, season, rural_producer
from app.api.v1.routes import router as api_router
from app.core.config import get_settings
from app.core.logging_config import LOGGING_CONFIG

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"
load_dotenv(dotenv_path=env_file)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info("Logger configured with success!")

settings = get_settings()

app = FastAPI(title="Rural Producers API", version="1.0.0", debug=settings.debug)

app.include_router(api_router, prefix="/api/v1")
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(crop.router, prefix="/api")
app.include_router(season.router, prefix="/api")
app.include_router(rural_producer.router, prefix="/api")
