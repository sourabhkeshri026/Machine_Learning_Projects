import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# -----------------------------------------------------
# LOAD BACKGROUND IMAGE
# -----------------------------------------------------

def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = BASE_DIR / "assets" / "background.png"

background_image = get_base64(BACKGROUND_PATH)

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:'Segoe UI';
}
            
*{

transition:.25s ease;

}

h1,h2,h3,h4,h5,h6,p,label{

color:white;

}

label{

font-weight:600;

font-size:15px;

letter-spacing:.3px;

}          

/* =====================================================
   APP BACKGROUND
===================================================== */

html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    background-image:
        linear-gradient(
            rgba(3, 10, 25, 0.28),
            rgba(3, 10, 25, 0.48)
        ),
        url("__BACKGROUND__") !important;

    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}

[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.block-container {
    background: transparent !important;
}

/* Remove Streamlit Menu */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

/* Header */

/* =====================================================
   HERO HEADER
===================================================== */

.main-header{

background:rgba(15,23,42,.45);

backdrop-filter:blur(24px);

-webkit-backdrop-filter:blur(24px);

border:1px solid rgba(255,255,255,.12);

border-radius:22px;

padding:22px 28px;

margin-bottom:18px;

box-shadow:0 10px 30px rgba(0,0,0,.30);

position:relative;

overflow:hidden;

}

.main-header::before{

content:"";

position:absolute;

top:-80px;

right:-80px;

width:220px;

height:220px;

background:rgba(96,165,250,.18);

border-radius:50%;

filter:blur(60px);

}

.main-header::after{

content:"";

position:absolute;

bottom:-70px;

left:-70px;

width:180px;

height:180px;

background:rgba(59,130,246,.18);

border-radius:50%;

filter:blur(60px);

}

.hero-title{

font-size:clamp(38px, 5vw, 58px);

font-weight:900;

color:white;

margin-bottom:10px;

text-align:center;

line-height:1.15;

letter-spacing:0.3px;

text-shadow:0 4px 18px rgba(0,0,0,.38);

}

.hero-subtitle{

font-size:20px;

font-weight:500;

color:#CBD5E1;

margin-bottom:10px;

text-align:center;

}

.hero-description{

font-size:15px;

line-height:1.6;

color:#E2E8F0;

max-width:900px;

}

.hero-stats{

display:flex;

gap:12px;

margin-top:18px;

flex-wrap:wrap;

}

.hero-box{

background:rgba(255,255,255,.06);

padding:12px 18px;

border-radius:14px;

border:1px solid rgba(255,255,255,.08);

min-width:120px;

text-align:center;

transition:.3s;

}

.hero-box:hover{

transform:translateY(-4px);

background:rgba(255,255,255,.10);

}

.hero-number{

font-size:22px;

font-weight:700;

color:#60A5FA;

}

.hero-label{

font-size:12px;

color:#CBD5E1;

margin-top:4px;

}
            
/* =====================================================
   LIVE KPI DASHBOARD
===================================================== */

.live-kpi{

background:rgba(255,255,255,.08);

backdrop-filter:blur(20px);

-webkit-backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.12);

border-radius:18px;

padding:22px;

text-align:center;

transition:.35s;

height:100%;

}

.live-kpi:hover{

transform:translateY(-6px);

background:rgba(255,255,255,.12);

box-shadow:0 15px 35px rgba(0,0,0,.30);

}

.live-kpi-value{

font-size:34px;

font-weight:700;

color:#60A5FA;

margin-bottom:10px;

}

.live-kpi-title{

font-size:15px;

font-weight:600;

color:white;

margin-bottom:8px;

}

.live-kpi-sub{

font-size:13px;

color:#CBD5E1;

}
            
/* =====================================================
   AI PREDICTION CONSOLE
===================================================== */

.ai-console{

background:rgba(255,255,255,.08);

backdrop-filter:blur(20px);

-webkit-backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.12);

border-radius:22px;

padding:24px;

height:100%;

box-shadow:0 12px 35px rgba(0,0,0,.25);

}

.console-title{

font-size:24px;

font-weight:700;

color:white;

margin-bottom:18px;

}

.console-card{

background:rgba(255,255,255,.06);

border-radius:14px;

padding:16px;

margin-bottom:15px;

border:1px solid rgba(255,255,255,.08);

}

.console-heading{

font-size:15px;

font-weight:600;

color:#60A5FA;

margin-bottom:8px;

}

.console-text{

font-size:14px;

color:#E2E8F0;

line-height:1.6;

}
            
/* =====================================================
   PREDICTION RESULT CARD
===================================================== */

.result-card{

background:linear-gradient(135deg,
rgba(37,99,235,.30),
rgba(59,130,246,.18));

backdrop-filter:blur(22px);

-webkit-backdrop-filter:blur(22px);

border:1px solid rgba(255,255,255,.14);

border-radius:22px;

padding:26px;

margin-top:18px;

box-shadow:0 18px 40px rgba(0,0,0,.28);

}

.result-title{

font-size:24px;

font-weight:700;

color:white;

margin-bottom:18px;

}

.result-value{

font-size:46px;

font-weight:800;

color:#60A5FA;

margin-bottom:8px;

}

.result-label{

font-size:16px;

color:#CBD5E1;

margin-bottom:18px;

}

.result-info{

background:rgba(255,255,255,.07);

padding:12px;

border-radius:12px;

margin-top:10px;

color:white;

}

/* =====================================================
   GLASS KPI CARD
===================================================== */

.metric-card{

background:rgba(255,255,255,.10);

backdrop-filter:blur(20px);

-webkit-backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.18);

border-radius:22px;

padding:25px;

text-align:center;

color:white;

box-shadow:0 12px 35px rgba(0,0,0,.30);

transition:all .35s ease;

overflow:hidden;

position:relative;

}

.metric-card::before{

content:"";

position:absolute;

top:0;

left:-120%;

width:70%;

height:100%;

background:linear-gradient(
90deg,
transparent,
rgba(255,255,255,.35),
transparent
);

transition:.8s;

}

.metric-card:hover::before{

left:150%;

}

.metric-card:hover{

transform:translateY(-10px) scale(1.02);

box-shadow:0 18px 45px rgba(0,0,0,.40);

}

.metric-card h2{

font-size:34px;

margin-bottom:10px;

background:linear-gradient(90deg,#60A5FA,#93C5FD);

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

font-weight:700;

}

.metric-card b{

font-size:16px;

font-weight:600;

}

/* =====================================================
   GLASS PREDICTION CARD
===================================================== */

.prediction-card{

background:rgba(255,255,255,.08);

backdrop-filter:blur(24px);

-webkit-backdrop-filter:blur(24px);

border:1px solid rgba(255,255,255,.16);

border-radius:24px;

padding:35px;

margin-top:20px;

box-shadow:0 15px 45px rgba(0,0,0,.35);

color:white;

transition:.35s;

}

.prediction-card:hover{

box-shadow:0 22px 55px rgba(0,0,0,.45);

}
            
/* =====================================================
   INPUT PANEL
===================================================== */

.input-panel{

background:rgba(255,255,255,.06);

backdrop-filter:blur(20px);

-webkit-backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.14);

border-radius:20px;

padding:25px;

margin-top:10px;

box-shadow:0 10px 35px rgba(0,0,0,.25);

}

/* =====================================================
   GLASS SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{

background:rgba(12,18,35,.55);

backdrop-filter:blur(22px);

-webkit-backdrop-filter:blur(22px);

border-right:1px solid rgba(255,255,255,.15);

}

section[data-testid="stSidebar"] *{

color:white;

}

/* =====================================================
   INPUT FIELDS
===================================================== */

div[data-baseweb="input"]{

background:rgba(255,255,255,.08);

border-radius:14px;

border:1px solid rgba(255,255,255,.12);

backdrop-filter:blur(15px);

}

div[data-baseweb="input"] input{

background:transparent !important;

color:white !important;

font-size:17px;

font-weight:500;

}

div[data-baseweb="input"]:focus-within{

border:1px solid #60A5FA;

box-shadow:0 0 18px rgba(96,165,250,.45);

}

/* =====================================================
   PREMIUM BUTTON
===================================================== */

.stButton>button{

width:100%;

height:55px;

border:none;

border-radius:14px;

font-size:17px;

font-weight:600;

color:white;

background:linear-gradient(135deg,#4F46E5,#2563EB);

transition:all .35s ease;

box-shadow:0 10px 25px rgba(37,99,235,.35);

}

.stButton>button:hover{

transform:translateY(-3px);

box-shadow:0 18px 35px rgba(37,99,235,.55);

background:linear-gradient(135deg,#2563EB,#1D4ED8);

}

/* =====================================================
   PLOTLY CHART
===================================================== */

.js-plotly-plot{

background:rgba(255,255,255,.05);

border-radius:20px;

padding:15px;

backdrop-filter:blur(18px);

}
            
/* =====================================================
   METRIC WIDGET
===================================================== */

div[data-testid="metric-container"]{

background:rgba(255,255,255,.08);

border:1px solid rgba(255,255,255,.15);

backdrop-filter:blur(18px);

border-radius:18px;

padding:15px;

box-shadow:0 10px 30px rgba(0,0,0,.25);

}

div[data-testid="metric-container"] label{

color:#D1D5DB;

}

div[data-testid="metric-container"] [data-testid="stMetricValue"]{

color:white;

font-size:30px;

font-weight:700;

}

/* Success */

.success-box{

background:rgba(34,197,94,.15);

border:1px solid rgba(34,197,94,.35);

backdrop-filter:blur(16px);

padding:20px;

border-radius:16px;

color:white;

}

.danger-box{

background:rgba(239,68,68,.15);

border:1px solid rgba(239,68,68,.35);

backdrop-filter:blur(16px);

padding:20px;

border-radius:16px;

color:white;

}



/* =====================================================
   RESULT POPUP DIALOG
===================================================== */

div[data-testid="stDialog"] > div {
    background: rgba(8, 15, 30, 0.96) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 22px !important;
    box-shadow: 0 28px 90px rgba(0,0,0,0.60) !important;
    backdrop-filter: blur(26px) !important;
    -webkit-backdrop-filter: blur(26px) !important;
}

div[data-testid="stDialog"] [data-testid="stVerticalBlock"] {
    gap: 0.8rem;
}

.popup-status-high {
    background: linear-gradient(135deg, rgba(239,68,68,.22), rgba(127,29,29,.28));
    border: 1px solid rgba(248,113,113,.45);
    border-radius: 16px;
    padding: 16px 18px;
    font-size: 18px;
    font-weight: 700;
    color: #FCA5A5;
}

.popup-status-low {
    background: linear-gradient(135deg, rgba(34,197,94,.20), rgba(20,83,45,.28));
    border: 1px solid rgba(74,222,128,.42);
    border-radius: 16px;
    padding: 16px 18px;
    font-size: 18px;
    font-weight: 700;
    color: #86EFAC;
}

.popup-recommendation {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 16px;
    padding: 18px 20px;
    min-height: 180px;
}

.popup-recommendation h4 {
    margin: 0 0 12px 0;
    color: white;
}

.popup-recommendation ul {
    margin: 0;
    padding-left: 20px;
    color: #E2E8F0;
    line-height: 1.9;
}

.invoice-form-shell {
    max-width: 820px;
    margin: 0 auto;
}

/* =====================================================
   RENDER / STREAMLIT 1.58 COMPATIBILITY OVERRIDES
===================================================== */

.main-header h1,
.main-header h2,
.main-header h3,
.main-header h4,
.prediction-card h1,
.prediction-card h2,
.prediction-card h3,
.input-panel h1,
.input-panel h2,
.input-panel h3,
.input-panel h4 {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label,
[data-testid="stForm"] label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stNumberInput"] div[data-baseweb="base-input"] {
    background: rgba(15, 23, 42, 0.82) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

[data-testid="stNumberInput"] input {
    background: transparent !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #60A5FA !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

[data-testid="stNumberInput"] button {
    background: rgba(30, 41, 59, 0.96) !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.10) !important;
}

[data-testid="stNumberInput"] button:hover {
    background: rgba(37, 99, 235, 0.95) !important;
    color: #FFFFFF !important;
}

[data-testid="stNumberInput"]:focus-within div[data-baseweb="input"],
[data-testid="stNumberInput"]:focus-within div[data-baseweb="base-input"] {
    border-color: #60A5FA !important;
    box-shadow: 0 0 0 1px #60A5FA, 0 0 18px rgba(96,165,250,.35) !important;
}

[data-testid="stForm"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 16px !important;
}

[data-testid="stFormSubmitButton"] button,
.stFormSubmitButton > button,
[data-testid="stButton"] button,
.stButton > button {
    width: 100% !important;
    min-height: 48px !important;
    border: 1px solid rgba(96,165,250,.35) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    background: linear-gradient(135deg,#4F46E5,#2563EB) !important;
    font-weight: 700 !important;
    box-shadow: 0 10px 25px rgba(37,99,235,.30) !important;
}

[data-testid="stDialog"],
div[role="dialog"] {
    color: #F8FAFC !important;
}

[data-testid="stDialog"] > div,
[data-testid="stDialog"] div[role="dialog"],
div[role="dialog"] {
    background: rgba(8, 15, 30, 0.98) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255,255,255,.16) !important;
    border-radius: 22px !important;
    box-shadow: 0 28px 90px rgba(0,0,0,.65) !important;
    backdrop-filter: blur(26px) !important;
    -webkit-backdrop-filter: blur(26px) !important;
}

[data-testid="stDialog"] h1,
[data-testid="stDialog"] h2,
[data-testid="stDialog"] h3,
[data-testid="stDialog"] h4,
[data-testid="stDialog"] p,
[data-testid="stDialog"] label,
[data-testid="stDialog"] span,
div[role="dialog"] h1,
div[role="dialog"] h2,
div[role="dialog"] h3,
div[role="dialog"] h4,
div[role="dialog"] p,
div[role="dialog"] label,
div[role="dialog"] span {
    color: #F8FAFC !important;
}

[data-testid="stDialog"] details,
div[role="dialog"] details {
    background: rgba(255,255,255,.035) !important;
    border: 1px solid rgba(255,255,255,.14) !important;
    border-radius: 12px !important;
}

[data-testid="stDialog"] [data-testid="stDataFrame"],
div[role="dialog"] [data-testid="stDataFrame"] {
    background: rgba(8,15,30,.86) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

[data-testid="stDialog"] [data-testid="stMetricLabel"],
[data-testid="stDialog"] [data-testid="stMetricValue"],
div[role="dialog"] [data-testid="stMetricLabel"],
div[role="dialog"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

</style>
""".replace("__BACKGROUND__", f"data:image/png;base64,{background_image}"),
unsafe_allow_html=True
)

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.markdown("""

<div class="main-header">

<div class="hero-title">

📦 Vendor Invoice Intelligence Portal

</div>

<div class="hero-subtitle">

AI-Powered Procurement Analytics Platform

</div>

<div class="hero-description">

Predict freight costs with machine learning, identify high-risk invoices before approval, and empower procurement teams with data-driven vendor intelligence.

</div>

<div class="hero-stats">

<div class="hero-box">

<div class="hero-number">96.5%</div>

<div class="hero-label">Freight Model R²</div>

</div>

<div class="hero-box">

<div class="hero-number">89%</div>

<div class="hero-label">Invoice Accuracy</div>

</div>

<div class="hero-box">

<div class="hero-number">2</div>

<div class="hero-label">ML Models</div>

</div>

<div class="hero-box">

<div class="hero-number">SQLite</div>

<div class="hero-label">Database</div>

</div>

</div>

</div>

""", unsafe_allow_html=True)

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

# c1,c2,c3,c4=st.columns(4)

# with c1:

#     st.markdown("""

# <div class="metric-card">

# <h2>96.5%</h2>

# <b>Freight Model R²</b>

# </div>

# """,unsafe_allow_html=True)

# with c2:

#     st.markdown("""

# <div class="metric-card">

# <h2>89%</h2>

# <b>Invoice Accuracy</b>

# </div>

# """,unsafe_allow_html=True)

# with c3:

#     st.markdown("""

# <div class="metric-card">

# <h2>2 Models</h2>

# <b>ML Pipelines</b>

# </div>

# """,unsafe_allow_html=True)

# with c4:

#     st.markdown("""

# <div class="metric-card">

# <h2>SQLite</h2>

# <b>Data Source</b>

# </div>

# """,unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------
# PROJECT HIGHLIGHTS
# -----------------------------------------------------

st.markdown("### 🚀 Project Highlights")

h1,h2,h3,h4 = st.columns(4)

cards=[
("⚙️","End-to-End ML Pipeline","Data preprocessing → Feature engineering → Training → Inference"),
("🤖","Two AI Models","Freight Cost Prediction & Invoice Risk Classification"),
("📊","Decision Support","Interactive prediction popups with business recommendations"),
("💼","Enterprise Stack","Python • Scikit-Learn • SQLite • Streamlit • Plotly")
]

for col,(icon,title,desc) in zip([h1,h2,h3,h4],cards):
    with col:
        st.markdown(f'''
        <div class="live-kpi">
            <div class="live-kpi-value" style="font-size:40px;">{icon}</div>
            <div class="live-kpi-title">{title}</div>
            <div class="live-kpi-sub">{desc}</div>
        </div>
        ''',unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.image(
    "https://img.icons8.com/color/96/artificial-intelligence.png",
    width=90
)

st.sidebar.title("Vendor Intelligence")

st.sidebar.markdown("---")

selected_model = st.sidebar.radio(

"Choose Prediction Module",

[
"🚚 Freight Cost Prediction",
"🚨 Invoice Risk Prediction"
]

)

st.sidebar.markdown("---")

st.sidebar.success("""

### Business Impact

✔ Better Vendor Negotiation

✔ Reduce Financial Leakage

✔ AI Powered Procurement

✔ Faster Invoice Processing

✔ Automated Risk Detection

""")

st.sidebar.markdown("---")

st.sidebar.info("""

Built Using

• Python

• SQL

• Scikit-Learn

• Streamlit

• Plotly

""")

# =====================================================
# INVOICE RESULT POPUP
# =====================================================

@st.dialog("Invoice Risk Assessment", width="large")
def show_invoice_result_dialog(
    prediction,
    flag,
    risk_score,
    invoice_quantity,
    invoice_dollars,
    freight,
    total_item_quantity,
    total_item_dollars
):
    """Display the complete invoice assessment inside a dismissible popup."""

    status_text = "HIGH RISK" if flag == 1 else "LOW RISK"
    decision_text = "Manual Review" if flag == 1 else "Auto Approval"
    status_class = "popup-status-high" if flag == 1 else "popup-status-low"
    status_icon = "🚨" if flag == 1 else "✅"

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Risk Score", f"{risk_score}%")
    metric_2.metric("Decision", decision_text)
    metric_3.metric("Invoice Value", f"${invoice_dollars:,.2f}")

    st.markdown(
        f'<div class="{status_class}">{status_icon} {status_text}</div>',
        unsafe_allow_html=True
    )

    chart_col, recommendation_col = st.columns([1.05, 1], gap="large")

    with chart_col:
        # Professional circular risk chart
        remaining_score = max(0, 100 - risk_score)

        if risk_score >= 70:
            risk_color = "#EF4444"
            risk_label = "High Risk"
        elif risk_score >= 40:
            risk_color = "#F59E0B"
            risk_label = "Moderate Risk"
        else:
            risk_color = "#22C55E"
            risk_label = "Low Risk"

        fig = go.Figure(
            data=[
                go.Pie(
                    values=[risk_score, remaining_score],
                    labels=["Risk Score", "Remaining"],
                    hole=0.72,
                    sort=False,
                    direction="clockwise",
                    rotation=90,
                    textinfo="none",
                    hoverinfo="skip",
                    marker={
                        "colors": [
                            risk_color,
                            "rgba(148,163,184,0.16)"
                        ],
                        "line": {
                            "color": "rgba(255,255,255,0.04)",
                            "width": 1
                        }
                    },
                    showlegend=False
                )
            ]
        )

        fig.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=18, b=18),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[
                {
                    "text": f"<b>{risk_score}%</b>",
                    "x": 0.5,
                    "y": 0.56,
                    "showarrow": False,
                    "font": {
                        "size": 38,
                        "color": "#F8FAFC"
                    }
                },
                {
                    "text": risk_label,
                    "x": 0.5,
                    "y": 0.40,
                    "showarrow": False,
                    "font": {
                        "size": 13,
                        "color": risk_color
                    }
                }
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "staticPlot": True
            }
        )

    with recommendation_col:
        if flag == 1:
            recommendation_html = """
            <div class="popup-recommendation">
                <h4>Recommended Action</h4>
                <ul>
                    <li>Route the invoice for manual approval.</li>
                    <li>Verify the vendor invoice against the purchase order.</li>
                    <li>Review freight charges for possible discrepancies.</li>
                    <li>Validate item quantities and total item value.</li>
                </ul>
            </div>
            """
        else:
            recommendation_html = """
            <div class="popup-recommendation">
                <h4>Recommended Action</h4>
                <ul>
                    <li>Invoice is suitable for automatic approval.</li>
                    <li>No abnormal activity was detected.</li>
                    <li>Invoice values appear consistent.</li>
                    <li>Continue with the standard payment workflow.</li>
                </ul>
            </div>
            """

        st.markdown(recommendation_html, unsafe_allow_html=True)

    with st.expander("View invoice details and model output"):
        details = pd.DataFrame(
            {
                "Field": [
                    "Invoice Quantity",
                    "Invoice Dollars",
                    "Freight",
                    "Total Item Quantity",
                    "Total Item Dollars",
                    "Predicted Flag"
                ],
                "Value": [
                    f"{invoice_quantity:,}",
                    f"${invoice_dollars:,.2f}",
                    f"${freight:,.2f}",
                    f"{total_item_quantity:,}",
                    f"${total_item_dollars:,.2f}",
                    int(flag)
                ]
            }
        )

        st.dataframe(
            details,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Close this assessment using the × icon in the upper-right corner of the popup."
    )


# =====================================================
# FREIGHT RESULT POPUP
# =====================================================

@st.dialog("Freight Cost Assessment", width="large")
def show_freight_result_dialog(
    prediction,
    quantity,
    dollars,
    freight
):
    """Display the freight prediction inside a dismissible popup."""

    freight_rate = (freight / dollars * 100) if dollars > 0 else 0
    landed_value = dollars + freight

    if freight_rate < 5:
        cost_level = "LOW COST"
        cost_label = "Efficient"
        status_class = "popup-status-low"
        chart_color = "#22C55E"
        status_icon = "✅"
    elif freight_rate < 12:
        cost_level = "MODERATE COST"
        cost_label = "Review"
        status_class = "popup-status-high"
        chart_color = "#F59E0B"
        status_icon = "⚠️"
    else:
        cost_level = "HIGH COST"
        cost_label = "High"
        status_class = "popup-status-high"
        chart_color = "#EF4444"
        status_icon = "🚨"

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Predicted Freight", f"${freight:,.2f}")
    metric_2.metric("Freight Rate", f"{freight_rate:.2f}%")
    metric_3.metric("Landed Value", f"${landed_value:,.2f}")

    st.markdown(
        f'<div class="{status_class}">{status_icon} {cost_level}</div>',
        unsafe_allow_html=True
    )

    chart_col, recommendation_col = st.columns([1.05, 1], gap="large")

    with chart_col:
        # Circular chart showing freight as a percentage of invoice value
        displayed_rate = min(max(freight_rate, 0), 100)
        remaining_rate = max(0, 100 - displayed_rate)

        fig = go.Figure(
            data=[
                go.Pie(
                    values=[displayed_rate, remaining_rate],
                    labels=["Freight Share", "Remaining"],
                    hole=0.72,
                    sort=False,
                    direction="clockwise",
                    rotation=90,
                    textinfo="none",
                    hoverinfo="skip",
                    marker={
                        "colors": [
                            chart_color,
                            "rgba(148,163,184,0.16)"
                        ],
                        "line": {
                            "color": "rgba(255,255,255,0.04)",
                            "width": 1
                        }
                    },
                    showlegend=False
                )
            ]
        )

        fig.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=18, b=18),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[
                {
                    "text": f"<b>{freight_rate:.1f}%</b>",
                    "x": 0.5,
                    "y": 0.56,
                    "showarrow": False,
                    "font": {
                        "size": 36,
                        "color": "#F8FAFC"
                    }
                },
                {
                    "text": "of invoice value",
                    "x": 0.5,
                    "y": 0.42,
                    "showarrow": False,
                    "font": {
                        "size": 12,
                        "color": "#94A3B8"
                    }
                },
                {
                    "text": cost_label,
                    "x": 0.5,
                    "y": 0.31,
                    "showarrow": False,
                    "font": {
                        "size": 13,
                        "color": chart_color
                    }
                }
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "staticPlot": True
            }
        )

    with recommendation_col:
        if freight_rate < 5:
            recommendation_html = """
            <div class="popup-recommendation">
                <h4>Recommended Action</h4>
                <ul>
                    <li>Freight cost is low relative to the invoice value.</li>
                    <li>Proceed with the standard procurement workflow.</li>
                    <li>Retain the prediction for cost benchmarking.</li>
                    <li>No immediate transport-cost intervention is required.</li>
                </ul>
            </div>
            """
        elif freight_rate < 12:
            recommendation_html = """
            <div class="popup-recommendation">
                <h4>Recommended Action</h4>
                <ul>
                    <li>Review carrier pricing and delivery terms.</li>
                    <li>Compare the shipment with similar purchase orders.</li>
                    <li>Check whether shipment consolidation is possible.</li>
                    <li>Validate the route and service level selected.</li>
                </ul>
            </div>
            """
        else:
            recommendation_html = """
            <div class="popup-recommendation">
                <h4>Recommended Action</h4>
                <ul>
                    <li>Investigate the unusually high freight-to-value ratio.</li>
                    <li>Review vendor shipment and carrier charges.</li>
                    <li>Consider route optimisation or shipment consolidation.</li>
                    <li>Negotiate revised freight terms before approval.</li>
                </ul>
            </div>
            """

        st.markdown(recommendation_html, unsafe_allow_html=True)

    with st.expander("View purchase details and model output"):
        details = pd.DataFrame(
            {
                "Field": [
                    "Quantity",
                    "Invoice Dollars",
                    "Predicted Freight",
                    "Freight Rate",
                    "Estimated Landed Value"
                ],
                "Value": [
                    f"{quantity:,}",
                    f"${dollars:,.2f}",
                    f"${freight:,.2f}",
                    f"{freight_rate:.2f}%",
                    f"${landed_value:,.2f}"
                ]
            }
        )

        st.dataframe(
            details,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Close this assessment using the × icon in the upper-right corner of the popup."
    )

# =====================================================
# FREIGHT COST PREDICTION
# =====================================================

if selected_model == "🚚 Freight Cost Prediction":

    st.markdown(
        """
        <div class="prediction-card">
            <h2>🚚 Freight Cost Prediction</h2>
            Enter the purchase details below. After prediction, the complete
            freight assessment will open in a focused popup window.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    form_left, form_center, form_right = st.columns([0.20, 0.60, 0.20])

    with form_center:

        st.markdown(
            """
            <div class="input-panel">
                <h3>📋 Purchase Details</h3>
                <p style="color:#CBD5E1; margin-top:-4px;">
                    Enter the quantity and invoice value to estimate transportation cost.
                </p>
            """,
            unsafe_allow_html=True
        )

        with st.form("freight_form"):

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1200,
                step=10
            )

            dollars = st.number_input(
                "Invoice Dollars ($)",
                min_value=1.0,
                value=18500.0,
                step=100.0
            )

            submit = st.form_submit_button(
                "🚀 Predict Freight Cost",
                use_container_width=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    if submit:

        input_data = {
            "Quantity": [quantity],
            "Dollars": [dollars]
        }

        prediction = predict_freight_cost(input_data)

        freight = float(
            prediction["Predicted_Freight"].iloc[0]
        )

        show_freight_result_dialog(
            prediction=prediction,
            quantity=quantity,
            dollars=dollars,
            freight=freight
        )

# =====================================================
# INVOICE RISK PREDICTION
# =====================================================

else:

    st.markdown(
        """
        <div class="prediction-card">
            <h2>🚨 Invoice Risk Prediction</h2>
            Enter the invoice values below. After evaluation, the complete
            risk assessment will open in a focused popup window.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    form_left, form_center, form_right = st.columns([0.15, 0.70, 0.15])

    with form_center:

        st.markdown(
            """
            <div class="input-panel">
                <h3>📝 Invoice Details</h3>
                <p style="color:#CBD5E1; margin-top:-4px;">
                    Complete all five fields and evaluate the invoice.
                </p>
            """,
            unsafe_allow_html=True
        )

        with st.form("invoice_form"):

            field_col_1, field_col_2 = st.columns(2, gap="large")

            with field_col_1:
                invoice_quantity = st.number_input(
                    "Invoice Quantity",
                    min_value=1,
                    value=50
                )

                invoice_dollars = st.number_input(
                    "Invoice Dollars ($)",
                    min_value=1.0,
                    value=352.95
                )

                freight = st.number_input(
                    "Freight ($)",
                    min_value=0.0,
                    value=1.73
                )

            with field_col_2:
                total_item_quantity = st.number_input(
                    "Total Item Quantity",
                    min_value=1,
                    value=162
                )

                total_item_dollars = st.number_input(
                    "Total Item Dollars ($)",
                    min_value=1.0,
                    value=2476.00
                )

                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

                submit = st.form_submit_button(
                    "🔍 Evaluate Invoice",
                    use_container_width=True
                )

        st.markdown("</div>", unsafe_allow_html=True)

    if submit:

        input_data = {
            "invoice_quantity": [invoice_quantity],
            "invoice_dollars": [invoice_dollars],
            "Freight": [freight],
            "total_item_quantity": [total_item_quantity],
            "total_item_dollars": [total_item_dollars]
        }

        prediction = predict_invoice_flag(input_data)
        flag = int(prediction["Predicted_Flag"].iloc[0])
        risk_score = 100 if flag == 1 else 10

        show_invoice_result_dialog(
            prediction=prediction,
            flag=flag,
            risk_score=risk_score,
            invoice_quantity=invoice_quantity,
            invoice_dollars=invoice_dollars,
            freight=freight,
            total_item_quantity=total_item_quantity,
            total_item_dollars=total_item_dollars
        )

# =====================================================
# ABOUT THIS PROJECT
# =====================================================

st.markdown("---")

st.markdown("""
<div class="prediction-card" style="padding:30px 32px;">
    <h2 style="margin-bottom:8px;">🧩 About This Project</h2>
    <p style="color:#CBD5E1; margin-bottom:0;">
        An end-to-end machine learning solution designed to support procurement
        teams with freight cost estimation and invoice risk assessment.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------
# SYSTEM ARCHITECTURE
# -----------------------------------------------------

st.markdown("### 🏗️ System Architecture")

arch1, arch2, arch3, arch4 = st.columns(4)

architecture_cards = [
    (
        "1",
        "Invoice Input",
        "User enters purchase and invoice details through the Streamlit interface."
    ),
    (
        "2",
        "Feature Processing",
        "Input values are prepared using the same structure used during model training."
    ),
    (
        "3",
        "ML Prediction",
        "Regression and classification models generate freight and invoice-risk outputs."
    ),
    (
        "4",
        "Business Decision",
        "The application converts predictions into clear procurement recommendations."
    )
]

for col, (step, title, description) in zip(
    [arch1, arch2, arch3, arch4],
    architecture_cards
):
    with col:
        st.markdown(
            f"""
            <div class="live-kpi" style="min-height:235px;">
                <div class="live-kpi-value"
                     style="
                        width:48px;
                        height:48px;
                        margin:0 auto 14px auto;
                        border-radius:50%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:21px;
                        background:rgba(59,130,246,.18);
                        border:1px solid rgba(96,165,250,.35);
                     ">
                    {step}
                </div>
                <div class="live-kpi-title">{title}</div>
                <div class="live-kpi-sub" style="line-height:1.6;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------
# PROJECT IMPACT
# -----------------------------------------------------

st.markdown("### 🎯 Business Impact")

impact1, impact2, impact3, impact4 = st.columns(4)

impact_cards = [
    ("💰","Cost Optimisation","Estimate freight costs before procurement decisions."),
    ("🛡️","Risk Reduction","Identify invoices that may require additional verification."),
    ("⚡","Faster Decisions","Support procurement teams with instant AI-assisted assessments."),
    ("📋","Better Governance","Promote consistent, transparent and data-driven approval workflows.")
]

for col, (icon, title, desc) in zip([impact1, impact2, impact3, impact4], impact_cards):
    with col:
        st.markdown(f'''
        <div class="live-kpi" style="min-height:220px;">
            <div class="live-kpi-value" style="font-size:40px;">{icon}</div>
            <div class="live-kpi-title">{title}</div>
            <div class="live-kpi-sub" style="line-height:1.6;">{desc}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------
# TECHNOLOGY STACK
# -----------------------------------------------------

st.markdown("### 🛠️ Technology Stack")

tech1, tech2, tech3, tech4, tech5 = st.columns(5)

technology_cards = [
    ("🐍", "Python", "Application and ML logic"),
    ("🧠", "Scikit-Learn", "Model training and inference"),
    ("🗄️", "SQLite", "Structured project database"),
    ("🖥️", "Streamlit", "Interactive web application"),
    ("📈", "Plotly", "Prediction visualisations")
]

for col, (icon, title, subtitle) in zip(
    [tech1, tech2, tech3, tech4, tech5],
    technology_cards
):
    with col:
        st.markdown(
            f"""
            <div class="live-kpi" style="min-height:190px;">
                <div class="live-kpi-value" style="font-size:38px;">{icon}</div>
                <div class="live-kpi-title">{title}</div>
                <div class="live-kpi-sub">{subtitle}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <hr>

    <center>

    <h4>📦 Vendor Invoice Intelligence Portal</h4>

    Built using Python • SQL • Scikit-Learn • Streamlit • Plotly

    <br>

    Developed by <b>Sourabh Kumar Keshri</b>

    MBA (Data Science & AI)

    Indian Institute of Technology (IIT) Mandi

    </center>

    """,
    unsafe_allow_html=True
)