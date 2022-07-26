from logging import NOTSET
from logging.config import dictConfig
from sys import stderr, stdout

from decouple import Choices, config

ALLOWED_LOG_LEVELS = Choices(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"])

PROJECT_NAME: str = config("PROJECT_NAME", default="aquila")
PROJECT_PORT: int = config("PROJECT_PORT", default=5000, cast=int)
DEBUG: bool = config("DEBUG", default=False, cast=bool)
ROOT_LOG_LEVEL: str = config("ROOT_LOG_LEVEL", default="ERROR", cast=ALLOWED_LOG_LEVELS)
LOG_FORMATTER: str = config("LOG_FORMATTER", default="json", cast=Choices(["brief", "json"]))

POLARIS_BASE_URL: str = config("POLARIS_BASE_URL", default="http://polaris-api/loyalty")

FETCH_TEMPLATES: bool = config("FETCH_TEMPLATES", default=True, cast=bool)
BLOB_STORAGE_DSN: str = config("BLOB_STORAGE_DSN")
BLOB_CONTAINER: str = config("BLOB_CONTAINER", default="aquila-templates")
BLOB_LOGGING_LEVEL: str = config("BLOB_LOGGING_LEVEL", default="ERROR", cast=ALLOWED_LOG_LEVELS)

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "brief": {"format": "%(levelname)s:     %(asctime)s - %(message)s"},
            "json": {"()": "app.reporting.JSONFormatter"},
        },
        "handlers": {
            "stderr": {
                "level": NOTSET,
                "class": "logging.StreamHandler",
                "stream": stderr,
                "formatter": LOG_FORMATTER,
            },
            "stdout": {
                "level": NOTSET,
                "class": "logging.StreamHandler",
                "stream": stdout,
                "formatter": LOG_FORMATTER,
            },
        },
        "loggers": {
            "root": {
                "level": ROOT_LOG_LEVEL,
                "handlers": ["stdout"],
            },
            "template-loader": {
                "level": BLOB_LOGGING_LEVEL,
                "handlers": ["stdout"],
            },
        },
    }
)
