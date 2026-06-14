# ratio_calculator.py
import pandas as pd


def to_float(value):
    if value is None:
        return None

    value = str(value).strip()

    if value.lower() in ["nan", "none", "null", "not found", "not_found", ""]:
        return None

    negative = False

    if value.startswith("(") and value.endswith(")"):
        negative = True
        value = value[1:-1]

    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.replace("INR", "")
    value = value.replace("Rs.", "")
    value = value.replace("Rs", "")
    value = value.replace("crores", "")
    value = value.replace("crore", "")
    value = value.replace("%", "")
    value = value.strip()

    try:
        number = float(value)

        if negative:
            number = -number

        return number

    except Exception:
        return None


def get_metric_value(structured_data, metric_key, field="current"):
    try:
        return to_float(structured_data["metrics"][metric_key][field])
    except Exception:
        return None


def safe_divide(numerator, denominator):
    if numerator is None or denominator is None:
        return None

    if denominator == 0:
        return None

    return numerator / denominator


def growth_percentage(current, previous):
    if current is None or previous is None:
        return None

    if previous == 0:
        return None

    return ((current - previous) / abs(previous)) * 100


def calculate_financial_ratios(structured_data):
    revenue = get_metric_value(structured_data, "revenue")
    revenue_previous = get_metric_value(structured_data, "revenue", "previous")

    total_income = get_metric_value(structured_data, "total_income")

    if revenue is None:
        revenue = total_income

    ebitda = get_metric_value(structured_data, "ebitda")
    pbt = get_metric_value(structured_data, "pbt")
    pat = get_metric_value(structured_data, "pat")
    pat_previous = get_metric_value(structured_data, "pat", "previous")

    current_assets = get_metric_value(structured_data, "current_assets")
    current_liabilities = get_metric_value(structured_data, "current_liabilities")
    inventories = get_metric_value(structured_data, "inventories")
    receivables = get_metric_value(structured_data, "trade_receivables")
    cash = get_metric_value(structured_data, "cash_and_cash_equivalents")

    short_term_borrowings = get_metric_value(structured_data, "short_term_borrowings")
    total_debt = get_metric_value(structured_data, "total_borrowings_debt")
    total_assets = get_metric_value(structured_data, "total_assets")
    total_equity = get_metric_value(structured_data, "total_equity")
    cfo = get_metric_value(structured_data, "cfo")
    capex = get_metric_value(structured_data, "capex")

    return {
        "Revenue Growth %": growth_percentage(revenue, revenue_previous),
        "PAT Growth %": growth_percentage(pat, pat_previous),
        "EBITDA Margin %": safe_divide(ebitda, revenue) * 100 if safe_divide(ebitda, revenue) is not None else None,
        "PBT Margin %": safe_divide(pbt, revenue) * 100 if safe_divide(pbt, revenue) is not None else None,
        "Net Profit Margin %": safe_divide(pat, revenue) * 100 if safe_divide(pat, revenue) is not None else None,
        "Current Ratio": safe_divide(current_assets, current_liabilities),
        "Quick Ratio": safe_divide(
            current_assets - inventories if current_assets is not None and inventories is not None else None,
            current_liabilities
        ),
        "Cash Ratio": safe_divide(cash, current_liabilities),
        "Receivables to Revenue %": safe_divide(receivables, revenue) * 100 if safe_divide(receivables, revenue) is not None else None,
        "Inventory to Revenue %": safe_divide(inventories, revenue) * 100 if safe_divide(inventories, revenue) is not None else None,
        "Debt to Assets": safe_divide(total_debt, total_assets),
        "Debt to Equity": safe_divide(total_debt, total_equity),
        "Short-Term Borrowings to Current Assets %": safe_divide(short_term_borrowings, current_assets) * 100 if safe_divide(short_term_borrowings, current_assets) is not None else None,
        "CFO to PAT": safe_divide(cfo, pat),
        "Free Cash Flow": cfo - capex if cfo is not None and capex is not None else None
    }


def determine_liquidity_rating(financial_ratios):
    current_ratio = financial_ratios.get("Current Ratio")
    quick_ratio = financial_ratios.get("Quick Ratio")
    cash_ratio = financial_ratios.get("Cash Ratio")
    cfo_to_pat = financial_ratios.get("CFO to PAT")
    debt_to_assets = financial_ratios.get("Debt to Assets")

    score = 0
    available = 0
    notes = []

    if current_ratio is not None:
        available += 1
        if current_ratio >= 2:
            score += 3
            notes.append("Current ratio is strong.")
        elif current_ratio >= 1.2:
            score += 2
            notes.append("Current ratio is adequate.")
        elif current_ratio >= 1:
            score += 1
            notes.append("Current ratio is just acceptable.")
        else:
            notes.append("Current ratio is weak.")

    if quick_ratio is not None:
        available += 1
        if quick_ratio >= 1:
            score += 3
            notes.append("Quick ratio is strong.")
        elif quick_ratio >= 0.75:
            score += 2
            notes.append("Quick ratio is adequate.")
        elif quick_ratio >= 0.5:
            score += 1
            notes.append("Quick ratio needs monitoring.")
        else:
            notes.append("Quick ratio is weak.")

    if cash_ratio is not None:
        available += 1
        if cash_ratio >= 0.5:
            score += 3
            notes.append("Cash ratio is strong.")
        elif cash_ratio >= 0.25:
            score += 2
            notes.append("Cash ratio is adequate.")
        elif cash_ratio >= 0.1:
            score += 1
            notes.append("Cash ratio needs monitoring.")
        else:
            notes.append("Cash ratio is weak.")

    if cfo_to_pat is not None:
        available += 1
        if cfo_to_pat >= 1:
            score += 3
            notes.append("Cash conversion is strong.")
        elif cfo_to_pat >= 0.7:
            score += 2
            notes.append("Cash conversion is adequate.")
        elif cfo_to_pat >= 0.4:
            score += 1
            notes.append("Cash conversion needs monitoring.")
        else:
            notes.append("Cash conversion is weak.")

    if debt_to_assets is not None:
        available += 1
        if debt_to_assets <= 0.1:
            score += 3
            notes.append("Debt burden is very low.")
        elif debt_to_assets <= 0.3:
            score += 2
            notes.append("Debt burden is moderate.")
        elif debt_to_assets <= 0.6:
            score += 1
            notes.append("Debt burden is high.")
        else:
            notes.append("Debt burden is critical.")

    if available == 0:
        return "Adequate", "Insufficient ratio data; rating is based on qualitative evidence only."

    average_score = score / available

    if average_score >= 2.4:
        rating = "Strong"
    elif average_score >= 1.6:
        rating = "Adequate"
    elif average_score >= 0.8:
        rating = "Weak"
    else:
        rating = "Critical"

    return rating, " ".join(notes)


def ratios_to_dataframe(financial_ratios):
    rows = []

    for key, value in financial_ratios.items():
        rows.append({
            "Ratio": key,
            "Value": "Not found" if value is None else round(value, 4)
        })

    return pd.DataFrame(rows)


def metrics_to_dataframe(structured_data):
    rows = []

    for key, item in structured_data.get("metrics", {}).items():
        rows.append({
            "Metric": key,
            "Label": item.get("label"),
            "Current": "Not found" if item.get("current") is None else item.get("current"),
            "Previous": "Not found" if item.get("previous") is None else item.get("previous"),
            "Unit": item.get("unit"),
            "Confidence": item.get("confidence"),
            "Source Quote": str(item.get("source_quote"))[:180] if item.get("source_quote") else "Not found"
        })

    return pd.DataFrame(rows)