import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.logger import log_info, log_error, log_debug
from utils.data_processor import (
    format_currency, 
    calculate_growth_rate, 
    get_trend_analysis,
    categorize_expenses
)
from data_loader import data_loader
from config import MENU_OPTIONS, CHART_COLORS, CURRENCY_SYMBOL

def show_metric_card(title, value, previous_value=None, prefix="", suffix=""):
    """Отображение метрики с изменением"""
    if previous_value:
        delta = calculate_growth_rate(value, previous_value)
        st.metric(
            title,
            f"{prefix}{format_currency(value, suffix)}",
            f"{delta:+.1f}%"
        )
    else:
        st.metric(title, f"{prefix}{format_currency(value, suffix)}")

def show_dashboard_page():
    """Главная страница дашборда"""
    st.title("📊 Панель управления")
    
    try:
        # Загрузка данных
        net_worth_summary = data_loader.get_net_worth_summary()
        income_summary = data_loader.get_income_summary()
        expenses_summary = data_loader.get_expenses_summary()
        budget_comparison = data_loader.get_budget_vs_actual()
        
        if not all([net_worth_summary, income_summary, expenses_summary, budget_comparison]):
            st.warning("⚠️ Загрузите файл с данными в разделе Настройки")
            return
        
        # Основные метрики
        col1, col2, col3 = st.columns(3)
        with col1:
            show_metric_card(
                "Чистая стоимость",
                net_worth_summary['current_net_worth'],
                suffix=CURRENCY_SYMBOL
            )
        with col2:
            show_metric_card(
                "Доходы (тек. месяц)",
                income_summary['monthly_history'].iloc[-1],
                income_summary['monthly_history'].iloc[-2],
                suffix=CURRENCY_SYMBOL
            )
        with col3:
            show_metric_card(
                "Расходы (тек. месяц)",
                expenses_summary['monthly_history'].iloc[-1],
                expenses_summary['monthly_history'].iloc[-2],
                suffix=CURRENCY_SYMBOL
            )
        
        # Графики
        col1, col2 = st.columns(2)
        
        with col1:
            show_mini_net_worth_chart(net_worth_summary['history'])
        with col2:
            show_mini_income_expenses_chart(
                income_summary['monthly_history'],
                expenses_summary['monthly_history']
            )
        
        col1, col2 = st.columns(2)
        with col1:
            show_mini_expense_breakdown(expenses_summary['by_category'])
        with col2:
            show_mini_budget_comparison(budget_comparison)
            
    except Exception as e:
        log_error(f"Ошибка при отображении дашборда: {str(e)}")
        st.error("Произошла ошибка при загрузке дашборда")

def show_net_worth_page():
    """Страница чистой стоимости"""
    st.title("💰 Чистая стоимость")
    
    try:
        net_worth_data = data_loader.get_net_worth_summary()
        if not net_worth_data:
            st.warning("⚠️ Нет данных о чистой стоимости")
            return
        
        # Основные метрики
        col1, col2, col3 = st.columns(3)
        with col1:
            show_metric_card(
                "Чистая стоимость",
                net_worth_data['current_net_worth'],
                suffix=CURRENCY_SYMBOL
            )
        with col2:
            show_metric_card(
                "Активы",
                net_worth_data['total_assets'],
                suffix=CURRENCY_SYMBOL
            )
        with col3:
            show_metric_card(
                "Обязательства",
                net_worth_data['total_liabilities'],
                suffix=CURRENCY_SYMBOL
            )
        
        # Детальный график
        show_detailed_net_worth_chart(net_worth_data['history'])
        
    except Exception as e:
        log_error(f"Ошибка при отображении страницы чистой стоимости: {str(e)}")
        st.error("Произошла ошибка при загрузке данных")

def show_income_expenses_page():
    """Страница доходов и расходов"""
    st.title("💵 Доходы и расходы")
    
    try:
        income_data = data_loader.get_income_summary()
        expenses_data = data_loader.get_expenses_summary()
        
        if not income_data or not expenses_data:
            st.warning("⚠️ Нет данных о доходах и расходах")
            return
        
        # Основные метрики
        col1, col2, col3 = st.columns(3)
        with col1:
            show_metric_card(
                "Общий доход",
                income_data['total_income'],
                suffix=CURRENCY_SYMBOL
            )
        with col2:
            show_metric_card(
                "Общие расходы",
                expenses_data['total_expenses'],
                suffix=CURRENCY_SYMBOL
            )
        with col3:
            balance = income_data['total_income'] - expenses_data['total_expenses']
            show_metric_card(
                "Баланс",
                balance,
                suffix=CURRENCY_SYMBOL
            )
        
        # Детальные графики
        show_detailed_income_expenses_chart(
            income_data['monthly_history'],
            expenses_data['monthly_history']
        )
        
        # Разбивка по источникам дохода и категориям расходов
        col1, col2 = st.columns(2)
        with col1:
            show_income_sources_chart(income_data['by_source'])
        with col2:
            show_expense_categories_chart(expenses_data['by_category'])
            
    except Exception as e:
        log_error(f"Ошибка при отображении страницы доходов и расходов: {str(e)}")
        st.error("Произошла ошибка при загрузке данных")

# ... продолжение следует ... 