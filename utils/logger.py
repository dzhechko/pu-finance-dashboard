from loguru import logger
import sys
from config import DEBUG, LOG_CONFIG

# Настройка логгера
logger.remove()  # Удаление стандартного обработчика

# Добавление обработчика для файла
if DEBUG:
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

# Добавление обработчика для консоли
logger.add(
    sys.stderr,
    level="INFO" if not DEBUG else "DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

def log_debug(message):
    """Логирование отладочной информации"""
    if DEBUG:
        logger.debug(message)

def log_info(message):
    """Логирование информационных сообщений"""
    logger.info(message)

def log_warning(message):
    """Логирование предупреждений"""
    logger.warning(message)

def log_error(message):
    """Логирование ошибок"""
    logger.error(message) 