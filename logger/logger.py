import logging
from logger.formatter import Formatter


#
class Logger:

    #
    def __init__(self, name: str) -> None:

        # Logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter())

        # File handler
        file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
        file_handler_formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
        )
        file_handler.setFormatter(file_handler_formatter)

        # Add the handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    #
    def debug(self, message: str) -> None:
        self.logger.debug(message)

    #
    def info(self, message: str) -> None:
        self.logger.info(message)

    #
    def warning(self, message: str) -> None:
        self.logger.warning(message)

    #
    def error(self, message: str) -> None:
        self.logger.error(message)

    #
    def critical(self, message: str) -> None:
        self.logger.critical(message)

    #
    def exception(self, message: str) -> None:
        self.logger.exception(message)

    #
    def log(self, level: int, message: str) -> None:
        self.logger.log(level, message)
