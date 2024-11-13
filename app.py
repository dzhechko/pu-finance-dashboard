import streamlit as st
from utils.logger import log_info, log_error
from config import DEBUG, AUTH, MENU_OPTIONS
import authentication
import dashboards
import data_loader

def main():
    st.set_page_config(
        page_title="Личные финансы",
        page_icon="💰",
        layout="wide"
    )
    
    log_info("Запуск приложения")
    
    # Инициализация состояния сессии
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = not AUTH

    try:
        # Обработка аутентификации
        if AUTH and not st.session_state.authenticated:
            authenticator, name = authentication.show_auth_page()
            if not st.session_state.get('authenticated', False):
                return

        # Отображение основного приложения
        if not AUTH or st.session_state.authenticated:
            show_main_app()

    except Exception as e:
        log_error(f"Ошибка приложения: {str(e)}")
        st.error("Произошла ошибка в приложении. Пожалуйста, попробуйте позже.")

def show_main_app():
    """Отображение основного интерфейса приложения"""
    with st.sidebar:
        st.title("💰 Личные финансы")
        
        if AUTH:
            st.write(f"👤 Пользователь: {st.session_state.username}")
            if st.button("Выйти"):
                authentication.logout()
        
        selected_page = st.radio(
            "Навигация",
            list(MENU_OPTIONS.keys()),
            format_func=lambda x: MENU_OPTIONS[x]
        )
    
    if selected_page == "dashboard":
        dashboards.show_dashboard_page()
    elif selected_page == "net_worth":
        dashboards.show_net_worth_page()
    elif selected_page == "income_expenses":
        dashboards.show_income_expenses_page()
    elif selected_page == "expense_breakdown":
        dashboards.show_expense_breakdown_page()
    elif selected_page == "budget":
        dashboards.show_budget_page()
    elif selected_page == "settings":
        show_settings_page()

def show_settings_page():
    """Отображение страницы настроек"""
    st.title(MENU_OPTIONS["settings"])
    
    if DEBUG:
        st.info("🐛 Режим отладки включен")
    
    with st.expander("📤 Загрузка данных"):
        st.write("""
        Загрузите Excel-файл со следующими листами:
        - Net Worth (Date, Assets, Liabilities)
        - Income (IncomeID, Date, Source, Amount)
        - Expenses (ExpenseID, Date, Category, Description, Amount)
        - Budget (Category, BudgetAmount)
        """)
        
        uploaded_file = st.file_uploader("Выберите файл Excel", type=['xlsx'])
        if uploaded_file:
            try:
                data_loader.process_uploaded_file(uploaded_file)
                st.success("✅ Файл успешно загружен!")
            except ValueError as ve:
                log_error(f"Ошибка валидации файла: {str(ve)}")
                st.error(f"❌ Ошибка в структуре файла: {str(ve)}")
            except Exception as e:
                log_error(f"Ошибка загрузки файла: {str(e)}")
                st.error("❌ Ошибка при загрузке файла. Проверьте формат данных.")

if __name__ == "__main__":
    main() 