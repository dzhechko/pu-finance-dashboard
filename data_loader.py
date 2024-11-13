import pandas as pd
import streamlit as st
from pathlib import Path
from utils.logger import log_info, log_error, log_debug, log_warning

# Определяем пути для сохранения данных
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

class DataLoader:
    """Класс для загрузки и обработки финансовых данных"""
    
    def __init__(self):
        self.data_file = DATA_DIR / "financial_data.xlsx"
        self.sheet_names = {
            'net_worth': 'Net Worth',
            'income': 'Income',
            'expenses': 'Expenses',
            'budget': 'Budget'
        }
    
    def validate_net_worth_data(self, df):
        """Проверка данных о чистой стоимости"""
        required_columns = ['Date', 'Assets', 'Liabilities']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Отсутствуют обязательные колонки: {required_columns}")
        
        # Проверка типов данных
        df['Date'] = pd.to_datetime(df['Date'])
        df['Assets'] = pd.to_numeric(df['Assets'])
        df['Liabilities'] = pd.to_numeric(df['Liabilities'])
        return df

    def validate_income_data(self, df):
        """Проверка данных о доходах"""
        required_columns = ['IncomeID', 'Date', 'Source', 'Amount']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Отсутствуют обязательные колонки: {required_columns}")
        
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'])
        return df

    def validate_expenses_data(self, df):
        """Проверка данных о расходах"""
        required_columns = ['ExpenseID', 'Date', 'Category', 'Description', 'Amount']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Отсутствуют обязательные колонки: {required_columns}")
        
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'])
        return df

    def validate_budget_data(self, df):
        """Проверка данных о бюджете"""
        required_columns = ['Category', 'BudgetAmount']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Отсутствуют обязательные колонки: {required_columns}")
        
        df['BudgetAmount'] = pd.to_numeric(df['BudgetAmount'])
        return df

    def process_uploaded_file(self, uploaded_file):
        """Обработка загруженного файла"""
        try:
            # Проверяем наличие всех необходимых листов
            xls = pd.ExcelFile(uploaded_file)
            missing_sheets = set(self.sheet_names.values()) - set(xls.sheet_names)
            
            if missing_sheets:
                raise ValueError(f"Отсутствуют необходимые листы: {missing_sheets}")
            
            # Читаем и валидируем каждый лист
            data_frames = {}
            for sheet_key, sheet_name in self.sheet_names.items():
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                
                # Валидация данных в зависимости от типа листа
                if sheet_key == 'net_worth':
                    df = self.validate_net_worth_data(df)
                elif sheet_key == 'income':
                    df = self.validate_income_data(df)
                elif sheet_key == 'expenses':
                    df = self.validate_expenses_data(df)
                elif sheet_key == 'budget':
                    df = self.validate_budget_data(df)
                
                data_frames[sheet_key] = df
            
            # Сохраняем все данные в один файл
            with pd.ExcelWriter(self.data_file) as writer:
                for sheet_key, df in data_frames.items():
                    df.to_excel(writer, sheet_name=self.sheet_names[sheet_key], index=False)
            
            log_info("Файл с финансовыми данными успешно обработан и сохранен")
            return True
            
        except Exception as e:
            log_error(f"Ошибка при обработке файла: {str(e)}")
            raise

    def load_data(self, data_type):
        """Загрузка данных определенного типа"""
        try:
            if not self.data_file.exists():
                log_warning("Файл с данными не найден")
                return None
            
            if data_type not in self.sheet_names:
                raise ValueError("Неизвестный тип данных")
            
            df = pd.read_excel(self.data_file, sheet_name=self.sheet_names[data_type])
            log_debug(f"Загружены данные типа {data_type}")
            return df
            
        except Exception as e:
            log_error(f"Ошибка при загрузке данных {data_type}: {str(e)}")
            return None

    def get_net_worth_summary(self):
        """Получение сводки по чистой стоимости"""
        df = self.load_data('net_worth')
        if df is None:
            return None
        
        df['NetWorth'] = df['Assets'] - df['Liabilities']
        latest = df.iloc[-1]
        return {
            'current_net_worth': latest['NetWorth'],
            'total_assets': latest['Assets'],
            'total_liabilities': latest['Liabilities'],
            'history': df
        }

    def get_income_summary(self, period='month'):
        """Получение сводки по доходам"""
        df = self.load_data('income')
        if df is None:
            return None
        
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_income = df.groupby('Month')['Amount'].sum()
        return {
            'total_income': df['Amount'].sum(),
            'average_monthly': monthly_income.mean(),
            'by_source': df.groupby('Source')['Amount'].sum(),
            'monthly_history': monthly_income
        }

    def get_expenses_summary(self, period='month'):
        """Получение сводки по расходам"""
        df = self.load_data('expenses')
        if df is None:
            return None
        
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_expenses = df.groupby('Month')['Amount'].sum()
        return {
            'total_expenses': df['Amount'].sum(),
            'average_monthly': monthly_expenses.mean(),
            'by_category': df.groupby('Category')['Amount'].sum(),
            'monthly_history': monthly_expenses
        }

    def get_budget_vs_actual(self):
        """Сравнение бюджета с фактическими расходами"""
        budget_df = self.load_data('budget')
        expenses_df = self.load_data('expenses')
        
        if budget_df is None or expenses_df is None:
            return None
        
        # Расчет фактических расходов по категориям
        actual = expenses_df.groupby('Category')['Amount'].sum()
        
        # Объединение с бюджетом
        comparison = pd.DataFrame({
            'Budget': budget_df.set_index('Category')['BudgetAmount'],
            'Actual': actual
        }).fillna(0)
        
        comparison['Difference'] = comparison['Budget'] - comparison['Actual']
        comparison['PercentUsed'] = (comparison['Actual'] / comparison['Budget'] * 100).round(2)
        
        return comparison

# Создание глобального экземпляра для использования в приложении
data_loader = DataLoader()

def process_uploaded_file(uploaded_file):
    """Обработка загруженного файла для использования в приложении"""
    try:
        success = data_loader.process_uploaded_file(uploaded_file)
        return success
    except Exception as e:
        log_error(f"Ошибка при обработке файла: {str(e)}")
        raise 