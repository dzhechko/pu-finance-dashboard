import pandas as pd
from utils.logger import log_debug, log_error

def calculate_growth_rate(current, previous):
    """Расчет темпа роста"""
    try:
        if previous == 0:
            return float('inf') if current > 0 else float('-inf') if current < 0 else 0
        return ((current - previous) / abs(previous)) * 100
    except Exception as e:
        log_error(f"Ошибка при расчете темпа роста: {str(e)}")
        return 0

def format_currency(amount, currency="₽"):
    """Форматирование денежных значений"""
    try:
        return f"{amount:,.2f} {currency}"
    except Exception as e:
        log_error(f"Ошибка при форматировании валюты: {str(e)}")
        return f"0.00 {currency}"

def calculate_moving_average(data, window=3):
    """Расчет скользящей средней"""
    try:
        return data.rolling(window=window).mean()
    except Exception as e:
        log_error(f"Ошибка при расчете скользящей средней: {str(e)}")
        return data

def get_trend_analysis(data):
    """Анализ тренда"""
    try:
        current = data.iloc[-1]
        previous = data.iloc[-2] if len(data) > 1 else current
        growth = calculate_growth_rate(current, previous)
        
        trend = "рост" if growth > 0 else "снижение" if growth < 0 else "стабильность"
        return {
            'trend': trend,
            'growth_rate': growth,
            'current': current,
            'previous': previous
        }
    except Exception as e:
        log_error(f"Ошибка при анализе тренда: {str(e)}")
        return None

def categorize_expenses(expenses_df, threshold=0.05):
    """Категоризация расходов с группировкой мелких категорий"""
    try:
        total_expenses = expenses_df['Amount'].sum()
        category_sums = expenses_df.groupby('Category')['Amount'].sum()
        
        # Определение основных и мелких категорий
        main_categories = category_sums[category_sums/total_expenses >= threshold]
        small_categories = category_sums[category_sums/total_expenses < threshold]
        
        # Объединение мелких категорий
        if not small_categories.empty:
            main_categories['Другое'] = small_categories.sum()
            
        return main_categories
    except Exception as e:
        log_error(f"Ошибка при категоризации расходов: {str(e)}")
        return None 