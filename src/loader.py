"""
CDAP - Corporate Data Analytics Platform
Модуль загрузки финансовых данных

Автор: Варданян Роберт Барсегович
Группа: БД251-м
Вариант: 9
"""

import pandas as pd
from pathlib import Path


# URL источника данных (Yahoo Finance API)
DATA_SOURCE_URL = "https://query1.finance.yahoo.com/v8/finance"

# Локальный путь к данным
DATA_DIR = Path(__file__).parent.parent / "data"


def load_financial_data(filepath: str = None) -> pd.DataFrame:
    """
    Загрузка финансовых данных из CSV файла.
    
    Args:
        filepath: Путь к файлу с данными. 
                  Если не указан, используется путь по умолчанию.
    
    Returns:
        DataFrame с финансовыми данными компаний.
    """
    if filepath is None:
        filepath = DATA_DIR / "financial_statements.csv"
    
    try:
        df = pd.read_csv(filepath)
        print(f"Загружено {len(df)} записей из {filepath}")
        return df
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        print(f"Скачайте данные с: {DATA_SOURCE_URL}")
        return pd.DataFrame()


def validate_required_columns(df: pd.DataFrame) -> bool:
    """
    Проверка наличия необходимых столбцов для расчёта ликвидности.
    
    Необходимые поля:
    - current_assets (оборотные активы)
    - current_liabilities (краткосрочные обязательства)
    - inventory (запасы)
    - cash (денежные средства)
    """
    required_columns = [
        'current_assets',
        'current_liabilities', 
        'inventory',
        'cash'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        print(f"Отсутствуют столбцы: {missing}")
        return False
    
    return True


def get_sample_data() -> pd.DataFrame:
    """
    Генерация тестовых данных для демонстрации.
    Используется когда реальные данные недоступны.
    """
    sample_data = {
        'company': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'],
        'current_assets': [500000, 750000, 300000, 1200000, 450000],
        'current_liabilities': [250000, 500000, 350000, 600000, 300000],
        'inventory': [100000, 200000, 80000, 300000, 120000],
        'cash': [150000, 180000, 50000, 400000, 100000],
        'year': [2024, 2024, 2024, 2024, 2024]
    }
    
    return pd.DataFrame(sample_data)


if __name__ == "__main__":
    print("=== CDAP Data Loader ===")
    print(f"Источник данных: {DATA_SOURCE_URL}")
    print()
    
    print("Тестовые данные:")
    sample = get_sample_data()
    print(sample.to_string(index=False))
