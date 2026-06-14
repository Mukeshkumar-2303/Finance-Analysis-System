# chart_generator.py
import os
import math
import matplotlib.pyplot as plt

from utils.ratio_calculator import get_metric_value, to_float


def create_key_metrics_chart(structured_data, output_path):
    selected_keys = [
        "revenue",
        "ebitda",
        "pbt",
        "pat",
        "current_assets",
        "current_liabilities",
        "cash_and_cash_equivalents",
        "trade_receivables",
        "inventories",
        "total_borrowings_debt",
        "cfo"
    ]

    labels = []
    values = []

    for key in selected_keys:
        item = structured_data.get("metrics", {}).get(key, {})
        value = to_float(item.get("current"))

        if value is not None:
            labels.append(item.get("label", key))
            values.append(value)

    if not values:
        return None

    plt.figure(figsize=(14, 6))
    plt.bar(labels, values)
    plt.title("Key Financial Metrics")
    plt.ylabel("Amount in INR crores")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    return output_path


def create_ratios_chart(financial_ratios, output_path):
    selected_ratios = {}

    for key, value in financial_ratios.items():
        if value is not None and isinstance(value, (int, float)) and not math.isnan(value):
            if key != "Free Cash Flow":
                selected_ratios[key] = value

    if not selected_ratios:
        return None

    plt.figure(figsize=(14, 6))
    plt.bar(selected_ratios.keys(), selected_ratios.values())
    plt.title("Financial Ratios")
    plt.ylabel("Ratio / Percentage")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    return output_path


def create_current_assets_pie_chart(structured_data, output_path):
    current_assets = get_metric_value(structured_data, "current_assets")
    inventories = get_metric_value(structured_data, "inventories")
    receivables = get_metric_value(structured_data, "trade_receivables")
    cash = get_metric_value(structured_data, "cash_and_cash_equivalents")

    if current_assets is None:
        return None

    components = {}

    if inventories is not None and inventories > 0:
        components["Inventories"] = inventories

    if receivables is not None and receivables > 0:
        components["Trade Receivables"] = receivables

    if cash is not None and cash > 0:
        components["Cash & Cash Equivalents"] = cash

    known_total = sum(components.values())
    other = current_assets - known_total

    if other > 0:
        components["Other Current Assets"] = other

    if not components:
        return None

    plt.figure(figsize=(7, 7))
    plt.pie(components.values(), labels=components.keys(), autopct="%1.1f%%")
    plt.title("Current Assets Composition")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    return output_path


def generate_all_charts(structured_data, financial_ratios, chart_dir):
    os.makedirs(chart_dir, exist_ok=True)

    key_metrics_chart = create_key_metrics_chart(
        structured_data,
        os.path.join(chart_dir, "key_financial_metrics.png")
    )

    ratios_chart = create_ratios_chart(
        financial_ratios,
        os.path.join(chart_dir, "financial_ratios.png")
    )

    assets_chart = create_current_assets_pie_chart(
        structured_data,
        os.path.join(chart_dir, "current_assets_composition.png")
    )

    return [
        chart for chart in [key_metrics_chart, ratios_chart, assets_chart]
        if chart is not None
    ]