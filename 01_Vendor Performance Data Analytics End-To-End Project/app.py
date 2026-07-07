import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

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

/* Background */

.stApp{
    background:#f4f7fb;
}

/* Remove Streamlit Menu */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

/* Header */

.main-header{

background:linear-gradient(135deg,#1d4ed8,#2563eb);

padding:35px;

border-radius:18px;

color:white;

box-shadow:0px 10px 30px rgba(0,0,0,.15);

margin-bottom:25px;

}

/* KPI Cards */

.metric-card{

background:white;

padding:20px;

border-radius:16px;

box-shadow:0px 8px 25px rgba(0,0,0,.08);

text-align:center;

transition:.3s;

}

.metric-card:hover{

transform:translateY(-6px);

box-shadow:0px 12px 30px rgba(0,0,0,.15);

}

/* Prediction Card */

.prediction-card{

background:white;

padding:30px;

border-radius:20px;

box-shadow:0px 12px 35px rgba(0,0,0,.10);

margin-top:20px;

}

/* Sidebar */

section[data-testid="stSidebar"]{

background:#1e293b;

color:white;

}

section[data-testid="stSidebar"] *{

color:white;

}

/* Buttons */

.stButton>button{

background:#2563eb;

color:white;

border-radius:12px;

height:52px;

font-size:18px;

font-weight:bold;

border:none;

}

.stButton>button:hover{

background:#1d4ed8;

}

/* Success */

.success-box{

background:#dcfce7;

padding:20px;

border-radius:12px;

}

/* Danger */

.danger-box{

background:#fee2e2;

padding:20px;

border-radius:12px;

}

</style>

""",unsafe_allow_html=True)

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.markdown("""

<div class="main-header">

<h1>📦 Vendor Invoice Intelligence Portal</h1>

<h4>AI Powered Procurement Intelligence Dashboard</h4>

<p>

Forecast Freight Costs • Detect Risky Invoices • Improve Vendor Operations

</p>

</div>

""",unsafe_allow_html=True)

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown("""

<div class="metric-card">

<h2>96.5%</h2>

<b>Freight Model R²</b>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown("""

<div class="metric-card">

<h2>89%</h2>

<b>Invoice Accuracy</b>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown("""

<div class="metric-card">

<h2>2 Models</h2>

<b>ML Pipelines</b>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown("""

<div class="metric-card">

<h2>SQLite</h2>

<b>Data Source</b>

</div>

""",unsafe_allow_html=True)

st.write("")

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
# FREIGHT COST PREDICTION
# =====================================================

if selected_model == "🚚 Freight Cost Prediction":

    st.markdown(
        """
        <div class="prediction-card">
        <h2>🚚 Freight Cost Prediction</h2>

        Predict the expected freight cost for a purchase order using
        machine learning trained on historical vendor invoices.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns([1,1])

    # -------------------------------
    # Input Section
    # -------------------------------

    with col1:

        st.subheader("📋 Enter Invoice Details")

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
                "🚀 Predict Freight Cost"
            )

    # -------------------------------
    # Prediction
    # -------------------------------

    with col2:

        st.subheader("📈 Prediction Dashboard")

        if submit:

            input_data = {
                "Quantity": [quantity],
                "Dollars": [dollars]
            }

            prediction = predict_freight_cost(input_data)

            freight = float(
                prediction["Predicted_Freight"].iloc[0]
            )

            # -----------------------
            # Gauge Chart
            # -----------------------

            fig = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=freight,

                    number={
                        "prefix":"$",
                        "font":{"size":40}
                    },

                    title={
                        "text":"Estimated Freight Cost"
                    },

                    gauge={

                        "axis":{
                            "range":[0,max(freight*2,500)]
                        },

                        "bar":{
                            "color":"royalblue"
                        },

                        "steps":[

                            {
                                "range":[0,max(freight*.6,100)],
                                "color":"#dcfce7"
                            },

                            {
                                "range":[
                                    max(freight*.6,100),
                                    max(freight*1.2,250)
                                ],
                                "color":"#fde68a"
                            },

                            {
                                "range":[
                                    max(freight*1.2,250),
                                    max(freight*2,500)
                                ],
                                "color":"#fecaca"
                            }

                        ]

                    }

                )

            )

            fig.update_layout(
                height=350,
                margin=dict(l=20,r=20,t=60,b=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.success("Prediction Completed Successfully!")

            st.metric(
                "Estimated Freight Cost",
                f"${freight:,.2f}"
            )

            # -----------------------
            # Business Insights
            # -----------------------

            st.markdown("---")

            st.subheader("💡 Business Insights")

            if freight < 100:

                st.success(
                    "Low Freight Cost.\n\n"
                    "No significant transportation concern detected."
                )

            elif freight < 300:

                st.warning(
                    "Moderate Freight Cost.\n\n"
                    "Review transportation efficiency."
                )

            else:

                st.error(
                    "High Freight Cost.\n\n"
                    "Investigate vendor shipment or route optimization."
                )

        else:

            st.info(
                "Enter invoice details and click **Predict Freight Cost**."
            )

    st.write("")

    # ---------------------------------------
    # Dashboard Summary
    # ---------------------------------------

    st.markdown("---")

    a,b,c = st.columns(3)

    with a:

        st.info("""
### 📦 Quantity

Number of units purchased from vendor.
""")

    with b:

        st.info("""
### 💰 Invoice Amount

Total purchase amount before freight.
""")

    with c:

        st.info("""
### 🚚 Freight Cost

Predicted transportation expense.
""")
# =====================================================
# INVOICE RISK PREDICTION
# =====================================================

else:

    st.markdown(
        """
        <div class="prediction-card">
        <h2>🚨 Invoice Risk Prediction</h2>

        Predict whether an invoice should be routed for
        <b>Manual Approval</b> using the trained Machine Learning model.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    left, right = st.columns([1, 1.2])

    # --------------------------------------------------
    # INPUTS
    # --------------------------------------------------

    with left:

        st.subheader("📝 Invoice Details")

        with st.form("invoice_form"):

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

            submit = st.form_submit_button(
                "🔍 Evaluate Invoice"
            )

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    with right:

        st.subheader("📊 Risk Dashboard")

        if submit:

            input_data = {

                "invoice_quantity":[invoice_quantity],

                "invoice_dollars":[invoice_dollars],

                "Freight":[freight],

                "total_item_quantity":[total_item_quantity],

                "total_item_dollars":[total_item_dollars]

            }

            prediction = predict_invoice_flag(input_data)

            flag = int(prediction["Predicted_Flag"].iloc[0])

            risk_score = 100 if flag == 1 else 10

            fig = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=risk_score,

                    number={"suffix":"%"},

                    title={"text":"Invoice Risk Score"},

                    gauge={

                        "axis":{"range":[0,100]},

                        "bar":{"color":"darkred"},

                        "steps":[

                            {
                                "range":[0,40],
                                "color":"#DCFCE7"
                            },

                            {
                                "range":[40,70],
                                "color":"#FDE68A"
                            },

                            {
                                "range":[70,100],
                                "color":"#FECACA"
                            }

                        ]

                    }

                )

            )

            fig.update_layout(height=350)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if flag == 1:

                st.error("🚨 HIGH RISK")

                st.markdown("""

### Recommendation

- Manual Approval Required

- Verify Vendor Invoice

- Check Freight Charges

- Validate Purchase Order

""")

            else:

                st.success("✅ LOW RISK")

                st.markdown("""

### Recommendation

- Safe for Auto Approval

- No abnormal activity detected

- Invoice appears consistent

""")

            st.markdown("---")

            st.subheader("Prediction Output")

            st.dataframe(
                prediction,
                use_container_width=True
            )

        else:

            st.info(
                "Fill in invoice details and click **Evaluate Invoice**."
            )

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

st.markdown("---")

st.subheader("📈 Business Value Delivered")

c1, c2, c3 = st.columns(3)

with c1:

    st.success("""

### 🚚 Freight Forecasting

Predict transportation costs before invoice approval.

""")

with c2:

    st.warning("""

### 🚨 Invoice Risk Detection

Automatically identify suspicious invoices.

""")

with c3:

    st.info("""

### 📊 Procurement Intelligence

Improve vendor management through AI-driven insights.

""")

# =====================================================
# TECHNOLOGY STACK
# =====================================================

st.markdown("---")

st.subheader("⚙ Technology Stack")

tech1, tech2, tech3, tech4, tech5 = st.columns(5)

tech1.metric("Python", "✓")

tech2.metric("SQLite", "✓")

tech3.metric("Scikit-Learn", "✓")

tech4.metric("Streamlit", "✓")

tech5.metric("Plotly", "✓")

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