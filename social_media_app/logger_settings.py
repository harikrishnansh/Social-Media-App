from social_media_app import settings

""" LOGGING SETTINGS FOR AUTHENTICATION SERVICE ERRORS AND OTHER RELATED LOGS. """


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "large": {
            "format": "%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  "
        },
        "tiny": {"format": "%(asctime)s  %(message)s  "},
    },
    "handlers": {
        "errors_file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "filename": settings.LOGGER_PATH + "/error_logger.log",
            "formatter": "large",
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "filename": settings.LOGGER_PATH + "/info_logger.log",
            "formatter": "large",
        },
    },
    "loggers": {
        "error_logger": {
            "handlers": ["errors_file"],
            "level": "WARNING",
            "propagate": False,
        },
        "info_logger": {
            "handlers": ["info_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
