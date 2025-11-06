from datetime import datetime


def fmt_dt_es(dt: datetime) -> str:
    # 05/11/2025 21:07
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def fmt_eur(n: int) -> str:
    # 1.234.567 €
    return f"{n:,.0f} €".replace(",", ".")