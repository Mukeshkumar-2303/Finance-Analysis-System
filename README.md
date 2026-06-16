# **FIN AI – Financial Statement Analysis System**

An AI-powered financial document analysis system built with Python, Streamlit, Gemini AI, PyMuPDF, pdfplumber, Pandas, Matplotlib, ReportLab, and python-docx.

This project analyzes company financial documents such as annual reports, quarterly results, balance sheets, and financial statements. It extracts financial data, calculates ratios, performs liquidity analysis, detects red flags, generates infographic charts, and exports professional PDF and Word reports.

---

![Screenshot](screenshot1.png)

---

## **FIN AI enables users to:**

* Upload financial documents in PDF, DOCX, or TXT format
* Analyze annual reports and financial statements
* Extract key financial metrics automatically
* Compare current year and previous year performance
* Calculate important financial ratios
* Generate liquidity risk ratings
* Identify financial red flags and positives
* Create infographic charts
* Export final analysis as PDF and Word reports

The system uses document extraction, AI-based structured data extraction, Python financial calculations, and automated report generation.

---

![Screenshot](screenshot2.png)

---

## **Features**

### AI-Powered Financial Document Understanding

* Reads financial statements and annual reports
* Extracts important financial values from unstructured text and tables
* Converts financial information into structured JSON
* Generates board-level financial analysis using Gemini AI

---

### Multi-Format Document Processing

The system supports:

* PDF financial reports
* Word documents
* Text files
* One or more uploaded documents

---

### PDF Text and Table Extraction

The project uses two PDF extraction libraries:

* **PyMuPDF** for fast page-wise text extraction
* **pdfplumber** for extracting financial tables such as balance sheets, profit and loss statements, and cash flow statements

This improves extraction quality because financial PDFs contain both paragraphs and complex tables.

---

### Financial Metrics Extraction

The system extracts key metrics such as:

* Revenue
* Total income
* Profit Before Tax
* Profit After Tax
* EBITDA
* EPS
* Current assets
* Current liabilities
* Inventories
* Trade receivables
* Cash and cash equivalents
* Borrowings
* Total assets
* Equity
* Cash flow from operations
* Capital expenditure
* Contingent liabilities

Each metric can include:

* Current year value
* Previous year value
* Unit
* Confidence
* Source quote

---

### Current Year vs Previous Year Comparison

The system compares financial values across years, helping users understand whether the company’s performance improved or weakened.

Examples:

* Revenue comparison
* PAT comparison
* Current assets comparison
* Current liabilities comparison
* Borrowings comparison
* Cash flow comparison

---

### Financial Ratio Calculation

Python is used to calculate ratios accurately using formulas.

Ratios include:

* Revenue Growth %
* PAT Growth %
* PBT Margin %
* Net Profit Margin %
* Current Ratio
* Quick Ratio
* Cash Ratio
* Receivables to Revenue %
* Inventory to Revenue %
* Debt to Assets
* Debt to Equity
* CFO to PAT
* Free Cash Flow

Using Python for calculations makes the system more reliable and reduces dependency on AI-generated calculations.

---

### Liquidity Risk Rating

The system assigns a liquidity risk rating based on financial ratios.

Possible ratings:

* Strong
* Adequate
* Weak
* Critical

The rating is based on:

* Current ratio
* Quick ratio
* Cash ratio
* CFO to PAT
* Debt burden

---

### AI-Generated Financial Analysis

The final AI report includes:

* Executive Summary
* Document Classification
* Financial Highlights
* Margin Trends
* Segmental / Geographical Performance
* Balance Sheet Analysis
* Cash Flow Analysis
* Detailed Liquidity Analysis
* Red Flags
* Positives
* Management Commentary
* Peer / Sector Context
* Board-Level Concerns
* Board Recommendations
* Early Warning Indicators
* Limitations

The AI is instructed not to invent values. If a value is not available in the uploaded document, the system marks it as not found.

---

### Infographic Chart Generation

The system generates charts using Matplotlib.

Charts include:

* Key Financial Metrics Chart
* Financial Ratios Chart
* Current Assets Composition Chart

These charts are included in the final report.

---

### Report Export

The project generates multiple output files:

* PDF financial analysis report
* Word financial analysis report
* Structured JSON data
* AI text report
* Chart images

---

## **System Workflow**

```text
Upload Financial Document
        ↓
Extract Text and Tables
        ↓
Filter Important Financial Sections
        ↓
Gemini AI Structured JSON Extraction
        ↓
Python Financial Ratio Calculation
        ↓
Liquidity Risk Rating
        ↓
Gemini AI Financial Analysis
        ↓
Generate Infographic Charts
        ↓
Export PDF / Word / JSON / Text Report
```

---

## **Architecture**

```text
                ┌──────────────────────────┐
                │        User Upload        │
                │   PDF / DOCX / TXT        │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │   Document Extraction     │
                │ PyMuPDF + pdfplumber      │
                │ python-docx               │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Financial Text Filtering  │
                │ Select important sections │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Gemini AI Extraction      │
                │ Text/Tables → JSON        │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Ratio Calculation Engine  │
                │ Python financial formulas │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Liquidity Risk Analysis   │
                │ Rule-based rating logic   │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ AI Report Generation      │
                │ Board-level analysis      │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Chart + Report Generator  │
                │ Matplotlib + ReportLab    │
                │ python-docx               │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Final Output              │
                │ PDF / Word / JSON / TXT   │
                └──────────────────────────┘
```

---

## **Tech Stack**

### Frontend

* Streamlit

### Backend

* Python

### AI / LLM

* Gemini AI
* google-genai

### Document Processing

* PyMuPDF
* pdfplumber
* python-docx

### Data Processing

* Pandas
* NumPy

### Visualization

* Matplotlib

### Report Generation

* ReportLab
* python-docx

### Environment Management

* python-dotenv

---

## **Folder Structure**

```text
Finance-Analysis-System/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── .env.example
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   ├── document_extractor.py
│   ├── ai_extractor.py
│   ├── ratio_calculator.py
│   ├── chart_generator.py
│   └── report_generator.py
│
├── outputs/
│   └── .gitkeep
│
├── temp/
│   └── .gitkeep
│
└── tests/
    └── test_ratio_calculator.py
```

---

## **Installation**

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Finance-Analysis-System
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **Environment Variables**

Create a `.env` file in the root folder.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not push the real `.env` file to GitHub.

Use `.env.example` as a sample file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## **Run the Application**

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

## **Usage**

1. Upload a financial document such as an annual report or financial statement.
2. Enter or load the Gemini API key.
3. Click the report generation button.
4. Wait while the system extracts text, tables, metrics, and ratios.
5. View extracted financial metrics and calculated ratios.
6. View generated charts.
7. Download the final PDF or Word report.

---

## **Example Use Cases**

* Analyze annual reports
* Compare current year and previous year performance
* Review company liquidity position
* Generate financial highlights
* Detect red flags in financial statements
* Prepare board-level financial review
* Convert long financial PDFs into readable reports
* Support financial research and credit analysis

---

## **Example Questions Answered by the Report**

```text
How did revenue change compared to the previous year?
Is the company’s liquidity position strong or weak?
Are current assets sufficient to cover current liabilities?
Is cash flow from operations supporting reported profit?
Are borrowings increasing?
What are the major financial red flags?
What should the board monitor?
```

---

## **Output Principle**

The system is designed to analyze only the information available in the uploaded financial document and optional context.

If a financial value is not found, the system clearly marks it as:

```text
Not found in uploaded document
```

This reduces hallucination and improves report reliability.

---

## **Limitations**

* Large annual reports may take more time to process
* PDF table extraction depends on the quality and layout of the PDF
* Scanned image PDFs may require OCR support
* AI-generated analysis should be reviewed before investment or business decisions
* Peer comparison depends on available uploaded or provided context
* The system is an analytical assistant, not a replacement for professional financial advice

---

## **Future Improvements**

* OCR support for scanned PDFs
* Peer company comparison
* NSE/BSE automatic filing fetch
* Industry benchmark comparison
* Financial trend dashboard
* More advanced forensic accounting checks
* Multi-company comparison
* Interactive chart dashboard
* Export to Excel
* Chat with financial report feature

---

## **Live Demo**

[Live Demo](https://finance-analysis-system-qnbhcucyupqjnlidetqmkr.streamlit.app/)

---

## **Author**

Built as an AI-powered financial document intelligence system for:

* Financial statement analysis
* Liquidity risk analysis
* Ratio calculation
* Financial report generation
* AI-assisted business insights

---

## **Disclaimer**

This project is for educational, analytical, and demonstration purposes. The generated report depends on extracted document content and AI interpretation. All financial values, conclusions, and recommendations should be verified before making investment, credit, business, or board-level decisions.
