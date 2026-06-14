import os
import json

import streamlit as st
from dotenv import load_dotenv

from utils.document_extractor import (
    extract_document,
    select_relevant_lines,
    select_relevant_table_rows,
)
from utils.ai_extractor import (
    get_gemini_client,
    call_gemini_json,
    call_gemini_text,
    build_structured_extraction_prompt,
    build_final_report_prompt,
)
from utils.ratio_calculator import (
    calculate_financial_ratios,
    determine_liquidity_rating,
    metrics_to_dataframe,
    ratios_to_dataframe,
)
from utils.chart_generator import generate_all_charts
from utils.report_generator import create_docx_report, create_pdf_report


# =========================================================
# PATH SETUP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)


# =========================================================
# LOAD ENV FILE
# =========================================================

ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="FIN AI Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DARK PROFESSIONAL UI CSS
# =========================================================

st.markdown(
    """
    <style>
    /* FULL APP BACKGROUND */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.20), transparent 32%),
            radial-gradient(circle at top right, rgba(14, 165, 233, 0.16), transparent 32%),
            linear-gradient(135deg, #020617 0%, #0f172a 50%, #111827 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #f8fafc !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 60%, #020617 100%);
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        background-color: #020617 !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    section[data-testid="stFileUploaderDropzone"] {
        background-color: #020617 !important;
        border: 1px dashed #475569 !important;
        border-radius: 18px !important;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: #f8fafc !important;
    }

    /* HERO */
    .hero-card {
        background:
            linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 58, 138, 0.92) 100%);
        padding: 2.6rem 2.4rem;
        border-radius: 30px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.38);
        border: 1px solid rgba(148, 163, 184, 0.28);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.22);
        color: #bfdbfe !important;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 800;
        margin-bottom: 0.9rem;
        border: 1px solid rgba(147, 197, 253, 0.35);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        margin-bottom: 0.75rem;
        letter-spacing: -0.04em;
        color: #ffffff !important;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.75;
        color: #dbeafe !important;
        max-width: 980px;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.94);
        padding: 0.65rem;
        border-radius: 18px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.30);
        border: 1px solid #334155;
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        background: #020617;
        border-radius: 14px;
        color: #cbd5e1 !important;
        font-weight: 850;
        padding: 0 18px;
        border: 1px solid #334155;
    }

    .stTabs [data-baseweb="tab"] p {
        color: #cbd5e1 !important;
        font-weight: 850;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid #60a5fa !important;
    }

    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }

    /* CUSTOM CARDS */
    .dark-card {
        background: rgba(15, 23, 42, 0.94);
        padding: 1.6rem;
        border-radius: 24px;
        border: 1px solid #334155;
        box-shadow: 0 22px 60px rgba(0, 0, 0, 0.30);
        margin-bottom: 1.2rem;
    }

    .metric-card {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        padding: 1.35rem;
        border-radius: 22px;
        border: 1px solid #334155;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
        min-height: 125px;
        margin-bottom: 0.7rem;
    }

    .metric-label {
        color: #94a3b8 !important;
        font-size: 0.9rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .metric-value {
        color: #ffffff !important;
        font-size: 1.45rem;
        font-weight: 900;
        margin-top: 0.3rem;
        word-break: break-word;
    }

    .workflow-card {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        border: 1px solid #334155;
        border-radius: 22px;
        padding: 1.35rem;
        min-height: 210px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
    }

    .workflow-title {
        color: #ffffff !important;
        font-size: 1.05rem;
        font-weight: 900;
        margin-bottom: 0.7rem;
    }

    .workflow-text {
        color: #cbd5e1 !important;
        font-size: 0.98rem;
        line-height: 1.75;
    }

    .section-title {
        color: #ffffff !important;
        font-size: 1.45rem;
        font-weight: 900;
        margin-bottom: 0.7rem;
    }

    .section-text {
        color: #cbd5e1 !important;
        font-size: 1rem;
        line-height: 1.75;
    }

    /* ALERTS */
    div[data-testid="stAlert"] {
        border-radius: 16px;
        border: 1px solid #334155;
        background: rgba(15, 23, 42, 0.95);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stAlert"] p {
        color: #f8fafc !important;
        font-weight: 700;
    }

    /* BUTTONS */
    .stButton > button {
        width: 100%;
        border-radius: 16px;
        padding: 0.85rem 1rem;
        font-weight: 900;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        box-shadow: 0 14px 35px rgba(37, 99, 235, 0.28);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 45px rgba(37, 99, 235, 0.38);
        color: white !important;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        padding: 0.85rem 1rem;
        font-weight: 900;
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white !important;
        border: none;
        box-shadow: 0 14px 35px rgba(22, 163, 74, 0.25);
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white !important;
    }

    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
        border: 1px solid #334155;
    }

    /* PROGRESS */
    [data-testid="stProgress"] > div {
        background-color: #1e293b;
    }

    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #2563eb, #22c55e);
    }

    /* IMAGES */
    [data-testid="stImage"] {
        background: #0f172a;
        padding: 1rem;
        border-radius: 22px;
        border: 1px solid #334155;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.28);
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(TEMP_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def get_api_key():
    env_key = os.getenv("GEMINI_API_KEY", "").strip()

    if env_key:
        st.success("✅ Gemini API key loaded from .env")

        sidebar_key = st.text_input(
            "Override Gemini API Key",
            type="password",
            help="Optional. Leave empty to use the key from .env.",
        )

        return sidebar_key.strip() or env_key

    st.warning("⚠️ Gemini API key not found in .env")

    sidebar_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Paste your Gemini API key here.",
    )

    return sidebar_key.strip()


def safe_display_value(value):
    if value is None:
        return "Not found"

    value = str(value)

    if value.lower() in ["nan", "none", "null", "not_found", ""]:
        return "Not found"

    return value


def display_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{safe_display_value(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_metric_current(structured_data, metric_key):
    try:
        return structured_data.get("metrics", {}).get(metric_key, {}).get("current")
    except Exception:
        return None


def run_analysis(uploaded_files, internet_context, api_key):
    combined_text = ""
    combined_tables_text = ""

    progress = st.progress(0)
    status = st.empty()

    status.info("Step 1/7: Saving and extracting documents...")

    for uploaded_file in uploaded_files:
        file_path = save_uploaded_file(uploaded_file)
        text, table_text, _ = extract_document(file_path)

        combined_text += f"""

==============================
DOCUMENT NAME: {uploaded_file.name}
==============================
{text}
"""

        combined_tables_text += f"""

==============================
TABLE DATA FROM: {uploaded_file.name}
==============================
{table_text}
"""

    progress.progress(15)

    status.info("Step 2/7: Preparing focused financial search pack...")

    financial_text_pack = select_relevant_lines(combined_text)
    financial_table_pack = select_relevant_table_rows(combined_tables_text)

    progress.progress(25)

    status.info("Step 3/7: Connecting to Gemini AI...")

    client = get_gemini_client(api_key)

    progress.progress(35)

    status.info("Step 4/7: Extracting structured financial data...")

    extraction_prompt = build_structured_extraction_prompt(
        financial_text_pack,
        financial_table_pack,
        internet_context,
    )

    structured_data = call_gemini_json(client, extraction_prompt)

    progress.progress(50)

    status.info("Step 5/7: Calculating financial ratios and liquidity rating...")

    financial_ratios = calculate_financial_ratios(structured_data)
    liquidity_rating, liquidity_rating_reason = determine_liquidity_rating(financial_ratios)

    metrics_df = metrics_to_dataframe(structured_data)
    ratios_df = ratios_to_dataframe(financial_ratios)

    progress.progress(65)

    status.info("Step 6/7: Creating infographic charts...")

    chart_paths = generate_all_charts(
        structured_data,
        financial_ratios,
        CHART_DIR,
    )

    progress.progress(78)

    status.info("Step 7/7: Generating AI report and output files...")

    final_report_prompt = build_final_report_prompt(
        structured_data,
        financial_ratios,
        liquidity_rating,
        liquidity_rating_reason,
    )

    ai_report = call_gemini_text(client, final_report_prompt)

    pdf_output_path = os.path.join(OUTPUT_DIR, "FIN_AI_Financial_Analysis_Report.pdf")
    docx_output_path = os.path.join(OUTPUT_DIR, "FIN_AI_Financial_Analysis_Report.docx")
    json_output_path = os.path.join(OUTPUT_DIR, "structured_financial_data.json")
    text_output_path = os.path.join(OUTPUT_DIR, "ai_financial_analysis_report.txt")

    create_pdf_report(
        pdf_output_path,
        structured_data,
        metrics_df,
        ratios_df,
        chart_paths,
        ai_report,
        liquidity_rating,
        liquidity_rating_reason,
    )

    create_docx_report(
        docx_output_path,
        structured_data,
        metrics_df,
        ratios_df,
        chart_paths,
        ai_report,
        liquidity_rating,
        liquidity_rating_reason,
    )

    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2)

    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write(ai_report)

    progress.progress(100)
    status.success("✅ Analysis completed successfully!")

    return {
        "structured_data": structured_data,
        "financial_ratios": financial_ratios,
        "metrics_df": metrics_df,
        "ratios_df": ratios_df,
        "liquidity_rating": liquidity_rating,
        "liquidity_rating_reason": liquidity_rating_reason,
        "chart_paths": chart_paths,
        "ai_report": ai_report,
        "pdf_output_path": pdf_output_path,
        "docx_output_path": docx_output_path,
        "json_output_path": json_output_path,
        "text_output_path": text_output_path,
    }


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-badge">AI Financial Document Intelligence</div>
        <div class="hero-title">📊 FIN AI Analyzer</div>
        <div class="hero-subtitle">
            Upload annual reports, quarterly results, balance sheets, or financial statements.
            FIN AI extracts financial metrics, calculates ratios, performs liquidity analysis,
            detects red flags, creates infographic charts, and generates professional PDF/Word reports.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("⚙️ Controls")
    st.caption("Upload financial documents and generate AI-powered reports.")

    api_key = get_api_key()

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload Financial Documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Upload one or more annual reports, quarterly results, or financial statements.",
    )

    internet_context = st.text_area(
        "Optional Internet Context",
        placeholder="Paste additional company/sector context here if needed...",
        height=120,
    )

    run_button = st.button("🚀 Generate Financial Report")


# =========================================================
# MAIN TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Overview",
        "📁 Upload",
        "📊 Results",
        "📈 Charts",
        "⬇️ Downloads",
    ]
)


# =========================================================
# OVERVIEW TAB
# =========================================================

with tab1:
    st.markdown(
        """
        <div class="dark-card">
            <div class="section-title">What this app does</div>
            <div class="section-text">
                FIN AI Analyzer reads financial documents, extracts text and table data,
                converts unstructured financial information into structured JSON, calculates financial ratios,
                generates liquidity analysis, detects red flags, and creates downloadable PDF/Word reports.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        display_metric_card("Input Types", "PDF / DOCX / TXT")
    with c2:
        display_metric_card("AI Engine", "Gemini")
    with c3:
        display_metric_card("Output", "PDF + Word")
    with c4:
        display_metric_card("Charts", "Infographics")

    st.markdown(
        """
        <div class="dark-card">
            <div class="section-title">Workflow</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    w1, w2, w3 = st.columns(3)

    with w1:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-title">1. Document Processing</div>
                <div class="workflow-text">
                    Upload annual reports, quarterly results, balance sheets, or financial statements.
                    The app extracts both normal text and financial tables.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with w2:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-title">2. AI + Ratio Engine</div>
                <div class="workflow-text">
                    Gemini converts extracted content into structured JSON.
                    Python calculates liquidity, margin, debt, and cash flow ratios.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with w3:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-title">3. Report Generation</div>
                <div class="workflow-text">
                    The app creates infographic charts and generates professional PDF/Word reports
                    with board-level recommendations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# UPLOAD TAB
# =========================================================

with tab2:
    st.markdown(
        """
        <div class="dark-card">
            <div class="section-title">Uploaded Documents</div>
            <div class="section-text">
                Upload one or more financial documents using the sidebar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

        for file in uploaded_files:
            st.write(f"✅ **{file.name}** — {round(file.size / (1024 * 1024), 2)} MB")
    else:
        st.info("Upload one or more files from the sidebar.")


# =========================================================
# RUN ANALYSIS
# =========================================================

if run_button:
    if not uploaded_files:
        st.error("Please upload at least one financial document.")
    elif not api_key:
        st.error("Please enter your Gemini API key or add it in `.env`.")
    else:
        try:
            with st.spinner("Running FIN AI analysis..."):
                result = run_analysis(uploaded_files, internet_context, api_key)
                st.session_state["result"] = result

        except Exception as e:
            st.error(f"Analysis failed: {e}")


# =========================================================
# RESULTS TAB
# =========================================================

with tab3:
    if "result" not in st.session_state:
        st.info("Run the analysis to view results.")
    else:
        result = st.session_state["result"]
        structured_data = result["structured_data"]
        classification = structured_data.get("classification", {})

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">Document Classification</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            display_metric_card("Company", classification.get("company_name"))
        with col2:
            display_metric_card("Fiscal Year", classification.get("fiscal_year"))
        with col3:
            display_metric_card("Liquidity Rating", result["liquidity_rating"])

        st.info(result["liquidity_rating_reason"])

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">Key Extracted Values</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            display_metric_card("Revenue", get_metric_current(structured_data, "revenue"))
        with k2:
            display_metric_card("PAT", get_metric_current(structured_data, "pat"))
        with k3:
            display_metric_card("Current Assets", get_metric_current(structured_data, "current_assets"))
        with k4:
            display_metric_card("Current Liabilities", get_metric_current(structured_data, "current_liabilities"))

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">Extracted Financial Metrics</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.dataframe(result["metrics_df"], use_container_width=True)

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">Calculated Financial Ratios</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.dataframe(result["ratios_df"], use_container_width=True)

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">AI Generated Financial Analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(result["ai_report"])


# =========================================================
# CHARTS TAB
# =========================================================

with tab4:
    if "result" not in st.session_state:
        st.info("Run the analysis to view charts.")
    else:
        result = st.session_state["result"]

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">Infographic Charts</div>
                <div class="section-text">
                    Visual summary of key metrics, calculated ratios, and current asset composition.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result["chart_paths"]:
            for chart_path in result["chart_paths"]:
                st.image(chart_path, use_container_width=True)
        else:
            st.warning("No charts generated because required values were not found.")


# =========================================================
# DOWNLOADS TAB
# =========================================================

with tab5:
    if "result" not in st.session_state:
        st.info("Run the analysis to download reports.")
    else:
        result = st.session_state["result"]

        st.markdown(
            """
            <div class="dark-card">
                <div class="section-title">Download Generated Reports</div>
                <div class="section-text">
                    Download the final financial analysis report in PDF or Word format.
                    You can also download the structured JSON and raw AI text report for verification.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            with open(result["pdf_output_path"], "rb") as f:
                st.download_button(
                    "⬇️ Download PDF Report",
                    data=f,
                    file_name="FIN_AI_Financial_Analysis_Report.pdf",
                    mime="application/pdf",
                )

        with col2:
            with open(result["docx_output_path"], "rb") as f:
                st.download_button(
                    "⬇️ Download Word Report",
                    data=f,
                    file_name="FIN_AI_Financial_Analysis_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

        col3, col4 = st.columns(2)

        with col3:
            with open(result["json_output_path"], "rb") as f:
                st.download_button(
                    "⬇️ Download Structured JSON",
                    data=f,
                    file_name="structured_financial_data.json",
                    mime="application/json",
                )

        with col4:
            with open(result["text_output_path"], "rb") as f:
                st.download_button(
                    "⬇️ Download AI Text Report",
                    data=f,
                    file_name="ai_financial_analysis_report.txt",
                    mime="text/plain",
                )