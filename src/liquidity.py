"""
CDAP - Corporate Data Analytics Platform
Расчёт коэффициентов ликвидности

Автор: Варданян Роберт Барсегович
Группа: БД251-м
Вариант: 9

Коэффициенты ликвидности:
1. Current Ratio (Текущая ликвидность) = Оборотные активы / Краткосрочные обязательства
2. Quick Ratio (Быстрая ликвидность) = (Оборотные активы - Запасы) / Краткосрочные обязательства  
3. Cash Ratio (Абсолютная ликвидность) = Денежные средства / Краткосрочные обязательства
"""

import pandas as pd
from loader import get_sample_data, load_financial_data


def calculate_current_ratio(current_assets: float, current_liabilities: float) -> float:
    """
    Коэффициент текущей ликвидности.
    Норма: 1.5 - 2.5
    """
    if current_liabilities == 0:
        return float('inf')
    return round(current_assets / current_liabilities, 2)


def calculate_quick_ratio(current_assets: float, inventory: float, 
                          current_liabilities: float) -> float:
    """
    Коэффициент быстрой ликвидности.
    Норма: 0.7 - 1.0
    """
    if current_liabilities == 0:
        return float('inf')
    return round((current_assets - inventory) / current_liabilities, 2)


def calculate_cash_ratio(cash: float, current_liabilities: float) -> float:
    """
    Коэффициент абсолютной ликвидности.
    Норма: 0.2 - 0.5
    """
    if current_liabilities == 0:
        return float('inf')
    return round(cash / current_liabilities, 2)


def analyze_liquidity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчёт всех коэффициентов ликвидности для DataFrame.
    
    Args:
        df: DataFrame с колонками: current_assets, current_liabilities, inventory, cash
        
    Returns:
        DataFrame с добавленными коэффициентами ликвидности
    """
    result = df.copy()
    
    result['current_ratio'] = df.apply(
        lambda row: calculate_current_ratio(
            row['current_assets'], 
            row['current_liabilities']
        ), axis=1
    )
    
    result['quick_ratio'] = df.apply(
        lambda row: calculate_quick_ratio(
            row['current_assets'],
            row['inventory'],
            row['current_liabilities']
        ), axis=1
    )
    
    result['cash_ratio'] = df.apply(
        lambda row: calculate_cash_ratio(
            row['cash'],
            row['current_liabilities']
        ), axis=1
    )
    
    return result


def interpret_liquidity(ratio_name: str, value: float) -> str:
    """
    Интерпретация значения коэффициента ликвидности.
    """
    interpretations = {
        'current_ratio': {
            'low': (0, 1.0, 'Критически низкая ликвидность'),
            'below_norm': (1.0, 1.5, 'Ниже нормы'),
            'norm': (1.5, 2.5, 'В пределах нормы'),
            'high': (2.5, float('inf'), 'Избыточная ликвидность')
        },
        'quick_ratio': {
            'low': (0, 0.5, 'Низкая ликвидность'),
            'below_norm': (0.5, 0.7, 'Ниже нормы'),
            'norm': (0.7, 1.0, 'В пределах нормы'),
            'high': (1.0, float('inf'), 'Высокая ликвидность')
        },
        'cash_ratio': {
            'low': (0, 0.1, 'Критически низкая'),
            'below_norm': (0.1, 0.2, 'Ниже нормы'),
            'norm': (0.2, 0.5, 'В пределах нормы'),
            'high': (0.5, float('inf'), 'Избыток денежных средств')
        }
    }
    
    if ratio_name not in interpretations:
        return 'Неизвестный коэффициент'
    
    for level, (low, high, description) in interpretations[ratio_name].items():
        if low <= value < high:
            return description
    
    return 'Не определено'


def print_liquidity_report(df: pd.DataFrame) -> None:
    """
    Вывод отчёта по ликвидности.
    """
    print("=" * 70)
    print("ОТЧЁТ ПО ЛИКВИДНОСТИ АКТИВОВ")
    print("=" * 70)
    print()
    
    for idx, row in df.iterrows():
        company = row.get('company', f'Компания {idx + 1}')
        print(f"Компания: {company}")
        print("-" * 40)
        
        current = row['current_ratio']
        quick = row['quick_ratio']
        cash = row['cash_ratio']
        
        print(f"  Текущая ликвидность:    {current:.2f} - {interpret_liquidity('current_ratio', current)}")
        print(f"  Быстрая ликвидность:    {quick:.2f} - {interpret_liquidity('quick_ratio', quick)}")
        print(f"  Абсолютная ликвидность: {cash:.2f} - {interpret_liquidity('cash_ratio', cash)}")
        print()
    
    print("=" * 70)
    print("Нормативные значения:")
    print("  Текущая ликвидность:    1.5 - 2.5")
    print("  Быстрая ликвидность:    0.7 - 1.0")
    print("  Абсолютная ликвидность: 0.2 - 0.5")
    print("=" * 70)


def get_liquidity_summary(df: pd.DataFrame) -> dict:
    """
    Краткая сводка по ликвидности всех компаний.
    Эта функция добавлена для демонстрации cherry-pick.
    """
    result = analyze_liquidity(df)
    return {
        'avg_current_ratio': round(result['current_ratio'].mean(), 2),
        'avg_quick_ratio': round(result['quick_ratio'].mean(), 2),
        'avg_cash_ratio': round(result['cash_ratio'].mean(), 2),
        'companies_analyzed': len(result)
    }


if __name__ == "__main__":
    print("=== CDAP: Анализ ликвидности активов ===")
    print()
    
    data = get_sample_data()
    result = analyze_liquidity(data)
    print_liquidity_report(result)
