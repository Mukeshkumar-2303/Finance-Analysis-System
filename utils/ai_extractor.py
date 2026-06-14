# ai_extractor.py
import json
from google import genai
from google.genai import types


MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]


def clean_json_response(text: str):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text


def get_gemini_client(api_key: str):
    if not api_key:
        raise ValueError("Gemini API key is missing.")
    return genai.Client(api_key=api_key)


def call_gemini_json(client, prompt: str):
    last_error = None

    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.05
                )
            )

            cleaned = clean_json_response(response.text)
            return json.loads(cleaned)

        except Exception as e:
            last_error = e

    raise Exception(f"Gemini JSON generation failed: {last_error}")


def call_gemini_text(client, prompt: str):
    last_error = None

    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2
                )
            )

            return response.text

        except Exception as e:
            last_error = e

    return f"Gemini text generation failed: {last_error}"


def build_structured_extraction_prompt(financial_text_pack, financial_table_pack, internet_context=""):
    return f"""
You are a highly accurate financial data extraction engine for Indian company financial statements.

TASK:
Extract clean structured financial data from uploaded financial documents.

STRICT RULES:
1. Return valid JSON only.
2. Do not invent numbers.
3. Use INR crores wherever possible.
4. Prefer consolidated figures if available.
5. If standalone and consolidated both exist, choose consolidated and mention basis.
6. Ignore page numbers, note numbers, serial numbers, section numbers, years, and unrelated percentages.
7. Extract actual values from balance sheet, profit and loss statement, cash flow statement, notes, or management discussion.
8. If a value is not clearly available, return null.
9. Every number must include source_quote.
10. Confidence must be high, medium, low, or not_found.

Return JSON in this exact structure:

{{
  "classification": {{
    "company_name": null,
    "document_type": null,
    "reporting_period": null,
    "fiscal_year": null,
    "basis": null,
    "industry": null
  }},
  "currency_unit": "INR crores",
  "metrics": {{
    "revenue": {{"label": "Revenue / Gross Revenue / Revenue from Operations", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "total_income": {{"label": "Total Income", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "ebitda": {{"label": "EBITDA", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "pbt": {{"label": "Profit Before Tax", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "pat": {{"label": "Profit After Tax / Profit for the Year", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "eps": {{"label": "Earnings Per Share", "current": null, "previous": null, "unit": "INR", "source_quote": null, "confidence": "not_found"}},
    "current_assets": {{"label": "Total Current Assets", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "inventories": {{"label": "Inventories", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "trade_receivables": {{"label": "Trade Receivables", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "cash_and_cash_equivalents": {{"label": "Cash and Cash Equivalents", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "current_liabilities": {{"label": "Total Current Liabilities", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "short_term_borrowings": {{"label": "Short-Term Borrowings / Current Borrowings", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "total_borrowings_debt": {{"label": "Total Borrowings / Total Debt", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "total_assets": {{"label": "Total Assets", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "total_equity": {{"label": "Total Equity", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "cfo": {{"label": "Net Cash Generated from Operating Activities", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "capex": {{"label": "Capital Expenditure / Purchase of PPE", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}},
    "contingent_liabilities": {{"label": "Contingent Liabilities / Claims Not Acknowledged as Debt", "current": null, "previous": null, "unit": "INR crores", "source_quote": null, "confidence": "not_found"}}
  }},
  "segments": [
    {{
      "segment_name": null,
      "revenue": null,
      "profit": null,
      "commentary": null,
      "source_quote": null
    }}
  ],
  "management_commentary": [],
  "risks": [],
  "positives": [],
  "data_quality_notes": []
}}

FINANCIAL TABLE PACK:
{financial_table_pack}

FINANCIAL TEXT PACK:
{financial_text_pack}

OPTIONAL INTERNET CONTEXT:
{internet_context[:12000]}
"""


def build_final_report_prompt(structured_data, financial_ratios, liquidity_rating, liquidity_rating_reason):
    return f"""
You are FinSight AI.

Act as:
1. Financial Analyst
2. Equity Research Analyst
3. Credit Risk Analyst
4. Independent Director
5. Forensic Accountant

Generate a professional board-level financial statement analysis report.

STRICT RULES:
- Use only the structured financial data and calculated ratios provided.
- Do not invent numbers.
- If data is missing, write "Not found in uploaded document".
- Use the calculated ratios exactly.
- Mention extraction limitations honestly.
- Highlight red flags, positives, and board concerns.
- Use Indian financial statement terminology.

STRUCTURED FINANCIAL DATA:
{json.dumps(structured_data, indent=2)}

CALCULATED RATIOS:
{json.dumps(financial_ratios, indent=2)}

LIQUIDITY RISK RATING:
{liquidity_rating}

LIQUIDITY RATING REASON:
{liquidity_rating_reason}

Generate the report in this exact structure:

1. EXECUTIVE SUMMARY
2. DOCUMENT CLASSIFICATION
3. FINANCIAL HIGHLIGHTS
4. MARGIN TRENDS
5. SEGMENTAL / GEOGRAPHICAL PERFORMANCE
6. BALANCE SHEET AND CASH FLOW ANALYSIS
7. DETAILED LIQUIDITY ANALYSIS FROM INDEPENDENT DIRECTOR PERSPECTIVE
7.1 CURRENT ASSETS COMPOSITION AND QUALITY
7.2 RECEIVABLES ANALYSIS
7.3 INVENTORY ANALYSIS
7.4 CURRENT LIABILITIES STRUCTURE
7.5 LIQUIDITY RATIOS CALCULATION
7.6 SHORT-TERM DEBT ANALYSIS
7.7 CASH FLOW CORRELATION
7.8 STRESS TESTING AND SCENARIO ANALYSIS
7.9 RED FLAGS AND WARNING SIGNS
7.10 CONTINGENT LIQUIDITY RISKS
7.11 LIQUIDITY MANAGEMENT ASSESSMENT
7.12 BOARD-LEVEL CONCERNS AND QUESTIONS
8. MANAGEMENT COMMENTARY AND GUIDANCE
9. RED FLAGS AND POSITIVES
10. PEER / SECTOR CONTEXT
11. LIQUIDITY RISK RATING
12. TOP 3 IMMEDIATE LIQUIDITY CONCERNS
13. BOARD RECOMMENDATIONS
14. EARLY WARNING INDICATORS TO MONITOR QUARTERLY
15. LIMITATIONS OF ANALYSIS
"""