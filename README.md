# Личные финансы - Дашборд

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/streamlit-personal-finance?referralCode=alphadash)

## 📊 О проекте

Веб-приложение для управления личными финансами, разработанное на Streamlit. Позволяет визуализировать и анализировать финансовые данные через интерактивные графики и отчеты.

### 🌟 Основные возможности

- **Авторизация пользователей**
  - Регистрация новых пользователей
  - Безопасный вход в систему
  - Восстановление пароля

- **Визуализация финансов**
  - График изменения чистой стоимости активов
  - Сравнение доходов и расходов
  - Разбивка расходов по категориям
  - Анализ бюджета и фактических трат

- **Управление данными**
  - Загрузка финансовых данных из Excel
  - Валидация и обработка данных
  - Автоматическое обновление графиков

### 📋 Требования к данным

Excel-файл должен содержать следующие листы:

1. **Net Worth**
   - Date: Дата
   - Assets: Активы
   - Liabilities: Обязательства

2. **Income**
   - IncomeID: ID дохода
   - Date: Дата
   - Source: Источник
   - Amount: Сумма

3. **Expenses**
   - ExpenseID: ID расхода
   - Date: Дата
   - Category: Категория
   - Description: Описание
   - Amount: Сумма

4. **Budget**
   - Category: Категория
   - BudgetAmount: Сумма бюджета

## 🚀 Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/personal-finance-dashboard.git
cd personal-finance-dashboard
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
streamlit run app.py
```

### Деплой на Railway.app

1. Нажмите кнопку "Deploy on Railway" выше
2. Войдите в свой аккаунт Railway
3. Следуйте инструкциям по настройке деплоя

## ⚙️ Настройка окружения

Создайте файл `.env` со следующими переменными:

```env
DEBUG=false
AUTH=true
PORT=8501
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
PYTHONUNBUFFERED=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_ENABLE_CORS=true
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

## 🔒 Безопасность

- Все пароли хешируются перед сохранением
- Поддержка CORS и XSRF-защиты
- Валидация всех входных данных

## 📱 Интерфейс

- Адаптивный дизайн
- Интерактивные графики
- Русскоязычный интерфейс
- Темная и светлая темы

## 🤝 Вклад в проект

Мы приветствуем ваш вклад в развитие проекта! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения и создайте pull request

## 📄 Лицензия

MIT License. Подробности в файле [LICENSE](LICENSE)

## 📞 Поддержка

- Создайте issue в репозитории
- Отправьте pull request с исправлением
- Свяжитесь с командой разработки

## 🙏 Благодарности

- [Streamlit](https://streamlit.io/) - за отличный фреймворк
- [Plotly](https://plotly.com/) - за интерактивные графики
- [Railway](https://railway.app/) - за простой деплой 