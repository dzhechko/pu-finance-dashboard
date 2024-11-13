import os
from pathlib import Path

# Debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Authentication enabled
AUTH = os.getenv("AUTH", "true").lower() == "true"

# Пути к данным
DATA_DIR = Path("data")
LOGS_DIR = Path("logs")

# Создание необходимых директорий
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Настройки логирования
LOG_CONFIG = {
    "DEBUG": DEBUG,
    "LOG_FILE": LOGS_DIR / "app.log",
    "MAX_SIZE": "500 MB",
    "RETENTION": "10 days"
}

# Меню на русском языке
MENU_OPTIONS = {
    "dashboard": "Панель управления",
    "net_worth": "Чистая стоимость",
    "income_expenses": "Доходы и расходы",
    "expense_breakdown": "Разбивка расходов",
    "budget": "Бюджет",
    "settings": "Настройки"
}

# Настройки валюты
CURRENCY_SYMBOL = "₽"
CURRENCY_FORMAT = "{:,.2f} ₽"

# Настройки графиков
CHART_COLORS = {
    "income": "#2ecc71",
    "expenses": "#e74c3c",
    "assets": "#3498db",
    "liabilities": "#e67e22",
    "net_worth": "#9b59b6"
}

# ... остальной код ... 