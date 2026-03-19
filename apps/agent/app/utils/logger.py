import logging
from rich.logging import RichHandler

def setup_logger(time: bool = True):
    if not time:
        return logging.basicConfig(
            format="{levelname}: {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            level=logging.INFO,
            handlers=[RichHandler()],
            force=True
        )

    return logging.basicConfig(
        format="{asctime} - {levelname}: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
        handlers=[RichHandler()],
        force=True
    )