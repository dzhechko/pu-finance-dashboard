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
import pandas as pd

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
        
        # Проверяем наличие данных
        if any(x is None for x in [net_worth_summary, income_summary, expenses_summary]):
            st.warning("⚠️ Загрузите файл с данными в разделе Настройки")
            return
            
        # Проверяем наличие необходимых данных в каждом summary
        if not isinstance(net_worth_summary.get('history'), pd.DataFrame):
            st.warning("⚠️ Нет данных о чистой стоимости")
            return
            
        if net_worth_summary['history'].empty:
            st.warning("⚠️ Нет данных о чистой стоимости")
            return
            
        if income_summary['monthly_history'].empty or expenses_summary['monthly_history'].empty:
            st.warning("⚠️ Нет данных о доходах и расходах")
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
        log_error(f"Ошибка при отбражении страницы чистой стоимости: {str(e)}")
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

def show_mini_net_worth_chart(df):
    """Мини-график чистой стоимости"""
    st.subheader("📈 Динамика чистой стоимости")
    
    fig = go.Figure()
    
    # Добавляем линии для активов, обязательств и чистой стоимости
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Assets'],
        name='Активы',
        line=dict(color=CHART_COLORS['assets'])
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Liabilities'],
        name='Обязательства',
        line=dict(color=CHART_COLORS['liabilities'])
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['NetWorth'],
        name='Чистая стоимость',
        line=dict(color=CHART_COLORS['net_worth'])
    ))
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Отображаем график без сохранения результата
    st.plotly_chart(fig, use_container_width=True)
    
    # Добавляем статический анализ последних данных
    latest = df.iloc[-1]
    st.info(f"""
    **Последние данные ({latest['Date'].strftime('%d.%m.%Y')}):**
    - Активы: {format_currency(latest['Assets'])}
    - Обязательства: {format_currency(latest['Liabilities'])}
    - Чистая стоимость: {format_currency(latest['NetWorth'])}
        """)

def show_mini_income_expenses_chart(income_data, expenses_data):
    """Мини-график доходов и расходов"""
    st.subheader("📊 Доходы и расходы по месяцам")
    
    # Создаем DataFrame для графика
    df = pd.DataFrame({
        'Доходы': income_data,
        'Расходы': expenses_data
    }).reset_index()
    df['Month'] = df['Month'].astype(str)
    
    fig = go.Figure()
    
    # Добавляем столбцы доходов и расходов
    fig.add_trace(go.Bar(
        x=df['Month'],
        y=df['Доходы'],
        name='Доходы',
        marker_color=CHART_COLORS['income']
    ))
    
    fig.add_trace(go.Bar(
        x=df['Month'],
        y=df['Расходы'],
        name='Расходы',
        marker_color=CHART_COLORS['expenses']
    ))
    
    fig.update_layout(
        height=400,
        barmode='group',
        hovermode='x unified',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Добавляем интерактивность
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    if selected_point:
        month = selected_point['points'][0]['x']
        row = df[df['Month'] == month].iloc[0]
        balance = row['Доходы'] - row['Расходы']
        
        st.info(f"""
        **Детали за {month}:**
        - Доходы: {format_currency(row['Доходы'])}
        - Расходы: {format_currency(row['Расходы'])}
        - Баланс: {format_currency(balance)}
        - Экономия: {(balance/row['Доходы']*100):.1f}% от дохода
        """)

def show_mini_expense_breakdown(expenses_by_category):
    """Мини-график разбивки расходов"""
    st.subheader("🍕 Структура расходов")
    
    # Группируем мелкие категории
    main_categories = categorize_expenses(expenses_by_category)
    
    fig = go.Figure(data=[go.Pie(
        labels=main_categories.index,
        values=main_categories.values,
        hole=.4,
        textinfo='percent+label'
    )])
    
    fig.update_layout(
        height=400,
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Добавляем интерактивность
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    if selected_point:
        category = selected_point['points'][0]['label']
        value = selected_point['points'][0]['value']
        percentage = selected_point['points'][0]['percent']
        
        st.info(f"""
        **Детали категории "{category}":**
        - Сумма: {format_currency(value)}
        - Доля в общих расходах: {percentage:.1f}%
        """)

def show_mini_budget_comparison(budget_data):
    """Мини-график сравнения бюджета с фактическими расходами"""
    st.subheader("📋 Бюджет vs Факт")
    
    fig = go.Figure()
    
    # Добавляем столбцы бюджета и фактических расходов
    fig.add_trace(go.Bar(
        x=budget_data.index,
        y=budget_data['Budget'],
        name='Бюджет',
        marker_color='rgba(46, 204, 113, 0.7)'
    ))
    
    fig.add_trace(go.Bar(
        x=budget_data.index,
        y=budget_data['Actual'],
        name='Факт',
        marker_color='rgba(231, 76, 60, 0.7)'
    ))
    
    fig.update_layout(
        height=400,
        barmode='group',
        hovermode='x unified',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Добавляем интерактивность
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    if selected_point:
        category = selected_point['points'][0]['x']
        row = budget_data.loc[category]
        
        status = "✅ В рамках бюджета" if row['Actual'] <= row['Budget'] else "❌ превышение бюджета"
        
        st.info(f"""
        **Детали категории "{category}":**
        - Бюджет: {format_currency(row['Budget'])}
        - Факт: {format_currency(row['Actual'])}
        - Разница: {format_currency(row['Difference'])}
        - Использовано: {row['PercentUsed']:.1f}% бюджета
        - Статус: {status}
        """)

def show_detailed_net_worth_chart(df):
    """Детальный график чистой стоимости"""
    st.subheader("📈 Детальный анализ чистой стоимости")
    
    # Добавляем фильтры периода
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Начальная дата",
            value=df['Date'].min(),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
    with col2:
        end_date = st.date_input(
            "Конечная дата",
            value=df['Date'].max(),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
    
    # Фильтруем данные
    mask = (df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))
    filtered_df = df[mask]
    
    # Создаем график
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Assets'],
        name='Активы',
        fill='tonexty',
        line=dict(color=CHART_COLORS['assets'])
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Liabilities'],
        name='Обязательства',
        fill='tonexty',
        line=dict(color=CHART_COLORS['liabilities'])
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['NetWorth'],
        name='Чистая стоимость',
        line=dict(color=CHART_COLORS['net_worth'], width=3)
    ))
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        showlegend=True,
        yaxis_title="Сумма",
        xaxis_title="Дата"
    )
    
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    # Добавляем анализ тренда
    trend = get_trend_analysis(filtered_df['NetWorth'])
    if trend:
        st.info(f"""
        **Анализ тренда:**
        - Текущий тренд: {trend['trend']}
        - Изменение: {trend['growth_rate']:+.1f}%
        - Текущее значение: {format_currency(trend['current'])}
        - Предыдущее значение: {format_currency(trend['previous'])}
        """)

def show_detailed_income_expenses_chart(income_data, expenses_data):
    """Детальный график доходов и расходов"""
    st.subheader("📊 Детальный анализ доходов и расходов")
    
    try:
        # Создаем DataFrame для графика
        df = pd.DataFrame({
            'Доходы': income_data,
            'Расходы': expenses_data
        }).reset_index()
        
        # Преобразуем Period в строку для корректного отображения
        df['Month'] = df['Month'].astype(str)
        
        # Добавляем фильтры периода
        months = df['Month'].unique().tolist()
        col1, col2 = st.columns(2)
        with col1:
            start_month = st.selectbox(
                "Начальный месяц",
                options=months,
                index=0
            )
        with col2:
            end_month = st.selectbox(
                "Конечный месяц",
                options=months,
                index=len(months)-1
            )
        
        # Фильтруем данные
        start_idx = months.index(start_month)
        end_idx = months.index(end_month)
        filtered_df = df.iloc[start_idx:end_idx+1]
        
        # Создаем график
        fig = go.Figure()
        
        # Добавляем линии доходов и расходов
        fig.add_trace(go.Scatter(
            x=filtered_df['Month'],
            y=filtered_df['Доходы'],
            name='Доходы',
            line=dict(color=CHART_COLORS['income'], width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=filtered_df['Month'],
            y=filtered_df['Расходы'],
            name='Расходы',
            line=dict(color=CHART_COLORS['expenses'], width=3)
        ))
        
        # Добавляем область между доходами и расходами
        fig.add_trace(go.Scatter(
            x=filtered_df['Month'],
            y=filtered_df['Доходы'] - filtered_df['Расходы'],
            name='Баланс',
            fill='tonexty',
            line=dict(color='rgba(0,100,0,0.3)')
        ))
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            showlegend=True,
            yaxis_title="Сумма",
            xaxis_title="Месяц"
        )
        
        selected_point = st.plotly_chart(fig, use_container_width=True)
        
        # Добавляем статистику
        st.subheader("📈 Статистика")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_income = filtered_df['Доходы'].mean()
            avg_expenses = filtered_df['Расходы'].mean()
            st.metric(
                "Средний месячный доход",
                format_currency(avg_income),
                f"{((filtered_df['Доходы'].iloc[-1] / avg_income - 1) * 100):+.1f}% к среднему"
            )
        
        with col2:
            st.metric(
                "Средние месячные расходы",
                format_currency(avg_expenses),
                f"{((filtered_df['Расходы'].iloc[-1] / avg_expenses - 1) * 100):+.1f}% к среднему"
            )
        
        with col3:
            savings_rate = ((filtered_df['Доходы'] - filtered_df['Расходы']) / filtered_df['Доходы'] * 100).mean()
            st.metric("Средняя норма сбережений", f"{savings_rate:.1f}%")

    except Exception as e:
        log_error(f"Ошибка при отображении страницы доходов и расходов: {str(e)}")
        st.error("Произошла ошибка при загрузке данных")

def show_income_sources_chart(income_by_source):
    """График источников дохода"""
    st.subheader("💰 Структура доходов")
    
    # Сортируем источники по убыванию дохода
    income_by_source_sorted = income_by_source.sort_values(ascending=True)
    
    # Создаем график
    fig = go.Figure(go.Bar(
        x=income_by_source_sorted.values,
        y=income_by_source_sorted.index,
        orientation='h',
        marker_color=CHART_COLORS['income']
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Сумма",
        yaxis_title="Источник"
    )
    
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    # Добавляем анализ
    total_income = income_by_source.sum()
    st.info(f"""
    **Анализ источников дохода:**
    - Общий доход: {format_currency(total_income)}
    - Основной источник: {income_by_source.idxmax()} ({(income_by_source.max() / total_income * 100):.1f}% от общего дохода)
    - Количество источников: {len(income_by_source)}
    """)

def show_expense_categories_chart(expenses_by_category):
    """График категорий расходов"""
    st.subheader("💸 Структура расходов")
    
    # Группируем мелкие категории
    main_categories = categorize_expenses(expenses_by_category)
    
    # Создаем круговую диаграмму
    fig = go.Figure(data=[go.Pie(
        labels=main_categories.index,
        values=main_categories.values,
        hole=.4,
        textinfo='percent+label',
        marker=dict(colors=px.colors.qualitative.Set3)
    )])
    
    fig.update_layout(
        height=500,
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    # Добавляем анализ
    total_expenses = expenses_by_category.sum()
    st.info(f"""
    **Анализ расходов:**
    - Общие расходы: {format_currency(total_expenses)}
    - Крупнейшая категория: {expenses_by_category.idxmax()} ({(expenses_by_category.max() / total_expenses * 100):.1f}% от общих расходов)
    - Количество категорий: {len(expenses_by_category)}
    """)

def show_expense_breakdown_page():
    """Страница разбивки расходов"""
    st.title("💸 Разбивка расходов")
    
    try:
        expenses_data = data_loader.get_expenses_summary()
        if expenses_data is None:
            st.warning("⚠️ Нет данных о расходах")
            return
            
        if expenses_data['by_category'].empty:
            st.warning("⚠️ Нет данных о категориях расходов")
            return
            
        # Основные метрики
        col1, col2, col3 = st.columns(3)
        with col1:
            show_metric_card(
                "Общие расходы",
                expenses_data['total_expenses'],
                suffix=CURRENCY_SYMBOL
            )
        with col2:
            show_metric_card(
                "Средние месячные расходы",
                expenses_data['average_monthly'],
                suffix=CURRENCY_SYMBOL
            )
        with col3:
            if len(expenses_data['monthly_history']) >= 2:
                current_month = expenses_data['monthly_history'].iloc[-1]
                prev_month = expenses_data['monthly_history'].iloc[-2]
                show_metric_card(
                    "Расходы в этом месяце",
                    current_month,
                    prev_month,
                    suffix=CURRENCY_SYMBOL
                )
            else:
                show_metric_card(
                    "Расходы в этом месяце",
                    expenses_data['monthly_history'].iloc[-1],
                    suffix=CURRENCY_SYMBOL
                )
        
        # Детальные графики
        show_expense_categories_chart(expenses_data['by_category'])
        
        # График трендов по месяцам
        st.subheader("📈 Тренды расходов по месяцам")
        show_detailed_expense_trends(expenses_data['monthly_history'])
        
    except Exception as e:
        log_error(f"Ошибка при отображении страницы расходов: {str(e)}")
        st.error("Произошла ошибка при загрузке данных")

def show_budget_page():
    """Страница бюджета"""
    st.title("📊 Бюджет")
    
    try:
        budget_data = data_loader.get_budget_vs_actual()
        if budget_data is None:
            st.warning("⚠️ Нет данных о бюджете")
            return
        
        # Основные метрики
        col1, col2, col3 = st.columns(3)
        with col1:
            total_budget = budget_data['Budget'].sum()
            total_actual = budget_data['Actual'].sum()
            show_metric_card(
                "Общий бюджет",
                total_budget,
                suffix=CURRENCY_SYMBOL
            )
        with col2:
            show_metric_card(
                "Фактические расходы",
                total_actual,
                suffix=CURRENCY_SYMBOL
            )
        with col3:
            budget_used = (total_actual / total_budget * 100)
            st.metric(
                "Использование бюджета",
                f"{budget_used:.1f}%",
                f"{100 - budget_used:.1f}% осталось"
            )
        
        # Детальное сравнение бюджета и фактических расходов
        show_detailed_budget_comparison(budget_data)
        
        # Анализ отклонений
        show_budget_variance_analysis(budget_data)
        
    except Exception as e:
        log_error(f"Ошибка при отображении страницы бюджета: {str(e)}")
        st.error("Произошла ошибка при загрузке данных")

def show_detailed_budget_comparison(budget_data):
    """Детальное сравнение бюджета с фактическими расходами"""
    st.subheader("📊 Сравнение бюджета и фактических расходов")
    
    # Создаем столбчатую диаграмму
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Бюджет',
        x=budget_data.index,
        y=budget_data['Budget'],
        marker_color='rgba(46, 204, 113, 0.7)'
    ))
    
    fig.add_trace(go.Bar(
        name='Факт',
        x=budget_data.index,
        y=budget_data['Actual'],
        marker_color='rgba(231, 76, 60, 0.7)'
    ))
    
    fig.update_layout(
        barmode='group',
        height=500,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Категория",
        yaxis_title="Сумма"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_budget_variance_analysis(budget_data):
    """Анализ отклонений от бюджета"""
    st.subheader("📉 Анализ отклонений")
    
    # Создаем DataFrame для анализа
    analysis = budget_data.copy()
    analysis['VariancePercent'] = (analysis['Actual'] - analysis['Budget']) / analysis['Budget'] * 100
    
    # Сортируем по абсолютному отклонению
    analysis = analysis.sort_values('VariancePercent', ascending=True)
    
    # Создаем график отклонений
    fig = go.Figure()
    
    colors = ['red' if x > 0 else 'green' for x in analysis['VariancePercent']]
    
    fig.add_trace(go.Bar(
        x=analysis.index,
        y=analysis['VariancePercent'],
        marker_color=colors
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Категория",
        yaxis_title="Отклонение (%)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Добавляем текстовый анализ
    over_budget = analysis[analysis['VariancePercent'] > 0]
    under_budget = analysis[analysis['VariancePercent'] < 0]
    
    if not over_budget.empty:
        st.warning(f"""
        **Превышение бюджета:**
        - {over_budget.index[0]}: +{over_budget['VariancePercent'].iloc[0]:.1f}%
        - {over_budget.index[1] if len(over_budget) > 1 else 'Нет'}: +{over_budget['VariancePercent'].iloc[1]:.1f}% (если есть)
        """)
    
    if not under_budget.empty:
        st.success(f"""
        **Экономия бюджета:**
        - {under_budget.index[0]}: {under_budget['VariancePercent'].iloc[0]:.1f}%
        - {under_budget.index[1] if len(under_budget) > 1 else 'Нет'}: {under_budget['VariancePercent'].iloc[1]:.1f}% (если есть)
        """)

def show_detailed_expense_trends(monthly_expenses):
    """График трендов расходов по месяцам"""
    try:
        # Создаем DataFrame для графика
        df = monthly_expenses.reset_index()
        df['Month'] = df['Month'].astype(str)
        
        fig = go.Figure()
        
        # Добавляем линию расходов
        fig.add_trace(go.Scatter(
            x=df['Month'],
            y=df['Amount'],
            name='Расходы',
            line=dict(color=CHART_COLORS['expenses'], width=2)
        ))
        
        # Добавляем скользящее среднее
        rolling_mean = df['Amount'].rolling(window=3, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=df['Month'],
            y=rolling_mean,
            name='Тренд (3 месяца)',
            line=dict(color='rgba(255, 165, 0, 0.7)', width=2, dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            showlegend=True,
            yaxis_title="Сумма",
            xaxis_title="Месяц"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Добавляем анализ тренда
        if len(df) >= 2:
            current = df['Amount'].iloc[-1]
            previous = df['Amount'].iloc[-2]
            change = ((current - previous) / previous * 100)
            
            if change > 0:
                st.warning(f"⚠️ Расходы выросли на {abs(change):.1f}% по сравнению с прошлым месяцем")
            elif change < 0:
                st.success(f"✅ Расходы снизились на {abs(change):.1f}% по сравнению с прошлым месяцем")
            else:
                st.info("ℹ️ Расходы остались на том же уровне")
                
    except Exception as e:
        log_error(f"Ошибка при отображении трендов расходов: {str(e)}")
        st.error("Не удалось отобразить тренды расходов")

# ... продолжение следует ... 