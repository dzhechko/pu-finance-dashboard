import streamlit as st
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
import streamlit_authenticator as stauth
from utils.logger import log_info, log_error, log_warning
import re

# Путь к файлу с учетными данными
CREDENTIALS_FILE = Path("credentials.yaml")

def is_valid_password(password):
    """Проверка надежности пароля"""
    if len(password) < 8:
        return False, "Пароль должен содержать минимум 8 символов"
    if not re.search(r"[A-Z]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    if not re.search(r"[a-z]", password):
        return False, "Пароль должен содержать хотя бы одну строчную букву"
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    return True, "Пароль соответствует требованиям"

def is_valid_username(username):
    """Проверка корректности имени пользователя"""
    if len(username) < 3:
        return False, "Имя пользователя должно содержать минимум 3 символа"
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Имя пользователя может содержать только буквы, цифры и знак подчеркивания"
    return True, "Имя пользователя корректно"

def load_credentials():
    """Загрузка учетных данных из файла"""
    if not CREDENTIALS_FILE.exists():
        default_credentials = {
            "usernames": {
                "admin": {
                    "name": "Админ",
                    "password": stauth.Hasher(['admin123']).generate()[0],
                    "email": "admin@example.com"
                }
            }
        }
        save_credentials(default_credentials)
        log_info("Создан файл credentials.yaml с учетными данными по умолчанию")
    
    with open(CREDENTIALS_FILE) as file:
        return yaml.load(file, Loader=SafeLoader)

def save_credentials(credentials):
    """Сохранение учетных данных в файл"""
    with open(CREDENTIALS_FILE, "w") as file:
        yaml.dump(credentials, file)
    log_info("Учетные данные успешно сохранены")

def register_user():
    """Форма регистрации нового пользователя"""
    st.subheader("📝 Регистрация нового пользователя")
    
    with st.form("registration_form"):
        new_username = st.text_input("Имя пользователя")
        new_name = st.text_input("Полное имя")
        new_email = st.text_input("Email")
        new_password = st.text_input("Пароль", type="password")
        confirm_password = st.text_input("Подтвердите пароль", type="password")
        
        submitted = st.form_submit_button("Зарегистрироваться")
        
        if submitted:
            credentials = load_credentials()
            
            # Проверка валидности данных
            username_valid, username_msg = is_valid_username(new_username)
            if not username_valid:
                st.error(username_msg)
                return
                
            if new_username in credentials["usernames"]:
                st.error("Пользователь с таким именем уже существует")
                return
                
            password_valid, password_msg = is_valid_password(new_password)
            if not password_valid:
                st.error(password_msg)
                return
                
            if new_password != confirm_password:
                st.error("Пароли не совпадают")
                return
            
            # Сохранение нового пользователя
            hashed_password = stauth.Hasher([new_password]).generate()[0]
            credentials["usernames"][new_username] = {
                "name": new_name,
                "password": hashed_password,
                "email": new_email
            }
            
            save_credentials(credentials)
            st.success("Регистрация успешно завершена! Теперь вы можете войти в систему.")
            log_info(f"Зарегистрирован новый пользователь: {new_username}")

def reset_password():
    """Форма восстановления пароля"""
    st.subheader("🔑 Восстановление пароля")
    
    with st.form("reset_password_form"):
        username = st.text_input("Имя пользователя")
        email = st.text_input("Email")
        new_password = st.text_input("Новый пароль", type="password")
        confirm_password = st.text_input("Подтвердите новый пароль", type="password")
        
        submitted = st.form_submit_button("Сбросить пароль")
        
        if submitted:
            credentials = load_credentials()
            
            if username not in credentials["usernames"]:
                st.error("Пользователь не найден")
                return
                
            if credentials["usernames"][username]["email"] != email:
                st.error("Указанный email не соответствует учетной записи")
                return
                
            password_valid, password_msg = is_valid_password(new_password)
            if not password_valid:
                st.error(password_msg)
                return
                
            if new_password != confirm_password:
                st.error("Пароли не совпадают")
                return
            
            # Обновление пароля
            hashed_password = stauth.Hasher([new_password]).generate()[0]
            credentials["usernames"][username]["password"] = hashed_password
            
            save_credentials(credentials)
            st.success("Пароль успешно обновлен! Теперь вы можете войти с новым паролем.")
            log_info(f"Пароль обновлен для пользователя: {username}")

def show_auth_page():
    """Отображение страницы аутентификации"""
    st.title("🔐 Авторизация")
    
    tab1, tab2, tab3 = st.tabs(["Вход", "Регистрация", "Восстановление пароля"])
    
    with tab1:
        authenticator, name = authenticate_users()
        return authenticator, name
    
    with tab2:
        register_user()
    
    with tab3:
        reset_password()

def authenticate_users():
    """Аутентификация пользователей"""
    credentials = load_credentials()
    authenticator = stauth.Authenticate(
        credentials,
        "personal_finance_dashboard",
        "auth_cookie",
        cookie_expiry_days=30
    )
    
    name, authentication_status, username = authenticator.login("Вход в систему", "main")
    
    if authentication_status:
        st.session_state.authenticated = True
        st.session_state.username = username
        log_info(f"Пользователь '{username}' вошел в систему")
        return authenticator, name
    elif authentication_status == False:
        st.error("❌ Неверное имя пользователя или пароль")
        log_warning(f"Неудачная попытка входа для пользователя '{username}'")
        return None, None
    elif authentication_status == None:
        st.info("👋 Пожалуйста, войдите в систему")
        return None, None

def logout():
    """Выход из системы"""
    if st.session_state.get('authenticated'):
        username = st.session_state.get('username')
        st.session_state.authenticated = False
        st.session_state.username = None
        log_info(f"Пользователь '{username}' вышел из системы")
        st.success("👋 Вы успешно вышли из системы")
        st.rerun() 