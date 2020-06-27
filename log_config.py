log_config = {
    "version": 1,
    "formatters": {
        "stream_formatter": {
            "format": "%(levelname)s - %(message)s"
        },
        "file_formatter": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%d-%m-%Y %H:%M",
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "stream_formatter",
            "level": "INFO",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "file_formatter",
            "level": "DEBUG",
            "filename": "bot.log",
            "encoding": "UTF-8",
        },
        "users_handler": {
            "class": "logging.FileHandler",
            "formatter": "file_formatter",
            "level": "INFO",
            "filename": "users.log",
            "encoding": "UTF-8",
        },
    },
    "loggers": {
        "file_stream": {
            "handlers": ["stream_handler", "file_handler"],
            "level": "DEBUG",
        },
        "users_handler": {
            "handlers": ["users_handler"],
            "level": "INFO",
        },
    },
}
