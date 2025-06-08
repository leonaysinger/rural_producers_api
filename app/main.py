import logging.config
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api.v1 import user, auth, crop, season, rural_producer, rural_property, report
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(x) for x in err["loc"])
        msg = err["msg"]
        errors.append({"field": loc, "message": msg})
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors},
    )

origins = [
    "http://localhost:5173",
    # "https://meusite.com.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(crop.router, prefix="/api")
app.include_router(season.router, prefix="/api")
app.include_router(rural_producer.router, prefix="/api")
app.include_router(rural_property.router, prefix="/api")
app.include_router(report.router, prefix="/api")
