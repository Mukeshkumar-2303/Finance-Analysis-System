# test_ratio_calculator.py
from utils.ratio_calculator import calculate_financial_ratios, determine_liquidity_rating


def test_ratio_calculation():
    sample_data = {
        "metrics": {
            "revenue": {"current": 1000, "previous": 800},
            "total_income": {"current": None, "previous": None},
            "ebitda": {"current": 200, "previous": None},
            "pbt": {"current": 150, "previous": None},
            "pat": {"current": 100, "previous": 80},
            "current_assets": {"current": 500, "previous": None},
            "inventories": {"current": 100, "previous": None},
            "trade_receivables": {"current": 150, "previous": None},
            "cash_and_cash_equivalents": {"current": 50, "previous": None},
            "current_liabilities": {"current": 250, "previous": None},
            "short_term_borrowings": {"current": 20, "previous": None},
            "total_borrowings_debt": {"current": 100, "previous": None},
            "total_assets": {"current": 1000, "previous": None},
            "total_equity": {"current": 700, "previous": None},
            "cfo": {"current": 120, "previous": None},
            "capex": {"current": 30, "previous": None},
        }
    }

    ratios = calculate_financial_ratios(sample_data)

    assert round(ratios["Revenue Growth %"], 2) == 25.00
    assert round(ratios["PAT Growth %"], 2) == 25.00
    assert round(ratios["EBITDA Margin %"], 2) == 20.00
    assert round(ratios["Current Ratio"], 2) == 2.00
    assert round(ratios["Quick Ratio"], 2) == 1.60
    assert round(ratios["Cash Ratio"], 2) == 0.20
    assert round(ratios["CFO to PAT"], 2) == 1.20


def test_liquidity_rating():
    ratios = {
        "Current Ratio": 2.0,
        "Quick Ratio": 1.2,
        "Cash Ratio": 0.4,
        "CFO to PAT": 1.1,
        "Debt to Assets": 0.1,
    }

    rating, reason = determine_liquidity_rating(ratios)

    assert rating in ["Strong", "Adequate", "Weak", "Critical"]
    assert isinstance(reason, str)