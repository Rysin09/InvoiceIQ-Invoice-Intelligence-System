import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go

st.set_page_config(
    page_title="InvoiceIQ",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# PREMIUM CSS
# --------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

:root {
    --bg:        #080C14;
    --surface:   #0D1420;
    --surface2:  #111927;
    --border:    rgba(255,255,255,0.07);
    --border-hi: rgba(99,202,183,0.35);
    --accent:    #63CAB7;
    --accent2:   #4F86F7;
    --danger:    #FF5A5A;
    --success:   #3DFFA0;
    --text:      #E8EDF5;
    --muted:     #6B7A99;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide Streamlit chrome completely ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; }

/* ── Hide sidebar collapse button + its "keyboard_do" tooltip ── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"],
[data-testid="stSidebar"] button,
[data-testid="stSidebarNav"] + div button,
.st-emotion-cache-zq5wmm,
[aria-label="collapse sidebar"],
[aria-label="open sidebar"] {
    display: none !important;
    visibility: hidden !important;
}

/* Nuke any tooltip/popover that contains the shortcut hint */
[data-testid="stTooltipHoverTarget"],
div[class*="Tooltip"],
div[class*="tooltip"] { display: none !important; }

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }

/* Radio items */
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important;
    font-weight: 400 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: var(--muted) !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    display: block !important;
    width: 100% !important;
    transition: background .15s, color .15s !important;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.04) !important;
    color: var(--text) !important;
}
/* Hide the default radio circle */
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── Sidebar brand logo (SVG-based, no clip-path issues) ── */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0 24px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 20px;
}
.sidebar-brand .brand-name {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 20px;
    color: #E8EDF5;
    letter-spacing: -0.3px;
    line-height: 1;
}
.sidebar-brand .brand-name span { color: #63CAB7; }

.sidebar-nav-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
    padding: 0 2px;
}

/* ── Page headers ── */
.eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 6px;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 40px;
    letter-spacing: -1px;
    line-height: 1.05;
    color: var(--text);
    margin: 0 0 8px 0;
}
.page-title em { font-style: normal; color: var(--accent); }
.page-sub {
    font-size: 14px;
    font-weight: 400;
    color: var(--muted);
    margin: 0 0 28px 0;
    line-height: 1.6;
}
.h-rule {
    height: 1px;
    background: linear-gradient(90deg, rgba(99,202,183,0.5) 0%, transparent 70%);
    margin-bottom: 32px;
}

/* ── KPI cards (via st.columns, styled per-column) ── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid;
    border-image: linear-gradient(90deg, #63CAB7, #4F86F7) 1;
    border-radius: 16px;
    padding: 22px 20px 18px 20px;
    height: 100%;
}
.kpi-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 30px;
    color: var(--text);
    letter-spacing: -0.5px;
    margin-bottom: 10px;
}
.kpi-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    background: rgba(99,202,183,0.12);
    color: var(--accent);
    border-radius: 6px;
    padding: 3px 10px;
}

/* ── Section heading ── */
.section-head {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* ── Form group label ── */
.form-group-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.form-group-title::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
}

/* ── Streamlit number input ── */
label, .stTextInput label, .stNumberInput label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}
input[type="number"] {
    background: var(--surface2) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
}
input[type="number"]:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,202,183,0.1) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, #63CAB7 0%, #4F86F7 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #080C14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    padding: 14px 28px !important;
    height: auto !important;
    width: 100% !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 4px 20px rgba(99,202,183,0.2) !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

/* ── Result cards ── */
.result-card {
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
}
.result-card.safe {
    background: rgba(61,255,160,0.05);
    border: 1px solid rgba(61,255,160,0.18);
}
.result-card.risk {
    background: rgba(255,90,90,0.05);
    border: 1px solid rgba(255,90,90,0.18);
}
.result-tag {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.result-tag.safe { color: #3DFFA0; }
.result-tag.risk { color: #FF5A5A; }
.result-headline {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 24px;
    letter-spacing: -0.3px;
    margin-bottom: 6px;
}
.result-headline.safe { color: #3DFFA0; }
.result-headline.risk { color: #FF5A5A; }
.result-desc {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 20px;
    line-height: 1.5;
}
.conf-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
}
.conf-track {
    height: 5px;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    overflow: hidden;
}
.conf-fill-safe {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #63CAB7, #3DFFA0);
}
.conf-fill-risk {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #FF5A5A, #FF8C42);
}

/* ── Freight cost display ── */
.cost-display {
    background: rgba(99,202,183,0.05);
    border: 1px solid rgba(99,202,183,0.18);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
}
.cost-tag {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 10px;
}
.cost-amount {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 44px;
    letter-spacing: -2px;
    color: var(--text);
    line-height: 1;
    margin-bottom: 10px;
}
.cost-amount sup {
    font-size: 22px;
    color: var(--accent);
    vertical-align: super;
    margin-right: 2px;
}
.cost-note {
    font-size: 12px;
    color: var(--muted);
}

/* ── Empty state ── */
.empty-state {
    height: 260px;
    background: var(--surface);
    border: 1px dashed rgba(255,255,255,0.08);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 10px;
    color: var(--muted);
    font-size: 13px;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(99,202,183,0.3) !important;
    border-radius: 10px !important;
    color: var(--accent) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    width: auto !important;
    padding: 10px 20px !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,202,183,0.07) !important;
    transform: none !important;
}

/* ── Info cards (dashboard model info) ── */
.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.info-card-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
}
.info-card-value {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: var(--text);
    margin-bottom: 3px;
}
.info-card-desc {
    font-size: 12px;
    color: var(--muted);
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# PATHS
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FREIGHT_MODEL_PATH = os.path.join(BASE_DIR, "freight_cost_prediction", "models", "predict_freight_model.pkl")
FLAG_MODEL_PATH    = os.path.join(BASE_DIR, "invoice_flagging",        "models", "predict_flag_invoice.pkl")
SCALER_PATH        = os.path.join(BASE_DIR, "invoice_flagging",        "models", "scaler.pkl")

# --------------------------
# LOAD MODELS
# --------------------------
@st.cache_resource
def load_models():
    freight_model = joblib.load(FREIGHT_MODEL_PATH)
    flag_model    = joblib.load(FLAG_MODEL_PATH)
    scaler        = joblib.load(SCALER_PATH)
    return freight_model, flag_model, scaler

freight_model, flag_model, scaler = load_models()

# --------------------------
# SIDEBAR  (SVG hex logo — no clip-path, renders everywhere)
# --------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="hg" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#63CAB7"/>
                    <stop offset="100%" stop-color="#4F86F7"/>
                </linearGradient>
            </defs>
            <polygon points="17,2 31,9.5 31,24.5 17,32 3,24.5 3,9.5" fill="url(#hg)"/>
            <text x="17" y="22" text-anchor="middle"
                  font-family="Syne,sans-serif" font-weight="800"
                  font-size="12" fill="#080C14">IQ</text>
        </svg>
        <div class="brand-name">Invoice<span>IQ</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-nav-label">Platform</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Dashboard", "Freight Prediction", "Invoice Risk Detection"],
        label_visibility="collapsed"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:16px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
                border-radius:12px; font-size:12px; color:#6B7A99; line-height:1.8;">
        <span style="font-family:'Syne',sans-serif; font-weight:700; color:#E8EDF5; font-size:13px;">
            InvoiceIQ v2.0
        </span><br>
        AI-powered freight &amp; risk analytics.<br>
        Models loaded · Ready for inference.
    </div>
    """, unsafe_allow_html=True)


# ============================
#  DASHBOARD
# ============================
if page == "Dashboard":

    st.markdown('<div class="eyebrow">Overview</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Intelligence <em>Dashboard</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Real-time AI freight prediction and invoice risk detection platform.</p>', unsafe_allow_html=True)
    st.markdown('<div class="h-rule"></div>', unsafe_allow_html=True)

    # KPI row — native st.columns so they render properly
    k1, k2, k3 = st.columns(3, gap="medium")
    with k1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Active Models</div>
            <div class="kpi-value">2</div>
            <div class="kpi-badge">Live</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Inference Mode</div>
            <div class="kpi-value">Real-Time</div>
            <div class="kpi-badge">Online</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Analytics Engine</div>
            <div class="kpi-value">Advanced</div>
            <div class="kpi-badge">Enabled</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-head">Module Utilisation</div>', unsafe_allow_html=True)

    col_chart, col_info = st.columns([3, 2], gap="large")

    with col_chart:
        # Donut chart — plain text annotation (no HTML in add_annotation)
        fig = go.Figure(go.Pie(
            labels=["Freight Prediction", "Invoice Risk Detection"],
            values=[65, 35],
            hole=0.70,
            marker=dict(
                colors=["#63CAB7", "#4F86F7"],
                line=dict(color="#080C14", width=4)
            ),
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=12, color="#E8EDF5"),
            hovertemplate="<b>%{label}</b><br>Share: %{value}%<extra></extra>"
        ))
        # Plain text annotation — no HTML tags
        fig.add_annotation(
            text="65 / 35",
            x=0.5, y=0.54,
            font=dict(family="Syne", size=22, color="#E8EDF5"),
            showarrow=False
        )
        fig.add_annotation(
            text="Module Split",
            x=0.5, y=0.42,
            font=dict(family="DM Sans", size=12, color="#6B7A99"),
            showarrow=False
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                font=dict(family="DM Sans", color="#6B7A99", size=12),
                bgcolor="rgba(0,0,0,0)",
                orientation="h",
                x=0.5, xanchor="center",
                y=-0.08
            ),
            height=380,
            margin=dict(t=20, b=10, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            <div class="info-card-label">Module 01 · Freight Model</div>
            <div class="info-card-value">Linear Regression</div>
            <div class="info-card-desc">Estimates freight cost from invoice value.</div>
        </div>
        <div class="info-card">
            <div class="info-card-label">Module 02 · Risk Model</div>
            <div class="info-card-value">Classification</div>
            <div class="info-card-desc">Flags anomalous or high-risk invoices.</div>
        </div>
        <div class="info-card">
            <div class="info-card-label">Preprocessing</div>
            <div class="info-card-value">StandardScaler</div>
            <div class="info-card-desc">Feature normalization for risk model inputs.</div>
        </div>
        """, unsafe_allow_html=True)


# ============================
#  FREIGHT PREDICTION
# ============================
elif page == "Freight Prediction":

    st.markdown('<div class="eyebrow">Module 01</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Freight Cost <em>Prediction</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter the invoice value to estimate expected freight cost using ML inference.</p>', unsafe_allow_html=True)
    st.markdown('<div class="h-rule"></div>', unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="form-group-title">Invoice Parameters</div>', unsafe_allow_html=True)

        dollars = st.number_input(
            "Invoice Dollars (USD)",
            min_value=0.0,
            value=10000.0,
            step=100.0,
            format="%.2f"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("Run Prediction →", key="freight_btn")

    with col_result:
        if run:
            input_df   = pd.DataFrame({"Dollars": [dollars]})
            prediction = freight_model.predict(input_df)[0]
            ratio      = (prediction / dollars * 100) if dollars > 0 else 0

            st.markdown(f"""
            <div class="cost-display">
                <div class="cost-tag">✦ Prediction Ready</div>
                <div style="font-size:12px; color:#6B7A99; margin-bottom:6px;">Estimated Freight Cost</div>
                <div class="cost-amount"><sup>$</sup>{prediction:,.2f}</div>
                <div class="cost-note">
                    Invoice value: <strong style="color:#E8EDF5">${dollars:,.2f}</strong>
                    &nbsp;·&nbsp; Freight ratio: <strong style="color:#63CAB7">{ratio:.1f}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(ratio, 2),
                number=dict(suffix="%", font=dict(family="Syne", color="#E8EDF5", size=26)),
                gauge=dict(
                    axis=dict(
                        range=[0, 20],
                        tickcolor="#6B7A99",
                        tickfont=dict(color="#6B7A99", size=10)
                    ),
                    bar=dict(color="#63CAB7", thickness=0.5),
                    bgcolor="rgba(0,0,0,0)",
                    borderwidth=0,
                    steps=[
                        dict(range=[0,  5],  color="rgba(61,255,160,0.07)"),
                        dict(range=[5,  10], color="rgba(79,134,247,0.07)"),
                        dict(range=[10, 20], color="rgba(255,90,90,0.07)")
                    ]
                ),
                title=dict(
                    text="Freight-to-Invoice Ratio",
                    font=dict(family="DM Sans", color="#6B7A99", size=12)
                )
            ))
            gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=200,
                margin=dict(t=40, b=10, l=30, r=30)
            )
            st.plotly_chart(gauge, use_container_width=True)

        else:
            st.markdown("""
            <div class="empty-state">
                <span style="font-size:32px; opacity:0.25;">◎</span>
                <span>Prediction will appear here</span>
            </div>
            """, unsafe_allow_html=True)


# ============================
#  INVOICE RISK DETECTION
# ============================
elif page == "Invoice Risk Detection":

    st.markdown('<div class="eyebrow">Module 02</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Invoice Risk <em>Detection</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Analyze invoice parameters to detect anomalies and flag high-risk transactions.</p>', unsafe_allow_html=True)
    st.markdown('<div class="h-rule"></div>', unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="form-group-title">Invoice Parameters</div>', unsafe_allow_html=True)

        invoice_quantity    = st.number_input("Invoice Quantity",    value=100,   step=1,   min_value=0)
        invoice_dollars     = st.number_input("Invoice Dollars",     value=10000, step=100, min_value=0)
        freight             = st.number_input("Freight",             value=150,   step=10,  min_value=0)
        total_item_quantity = st.number_input("Total Item Quantity", value=100,   step=1,   min_value=0)
        total_item_dollars  = st.number_input("Total Item Dollars",  value=9998,  step=100, min_value=0)

        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button("Analyze Invoice →", key="flag_btn")

    with col_result:
        if analyze:
            df = pd.DataFrame({
                "invoice_quantity":    [invoice_quantity],
                "invoice_dollars":     [invoice_dollars],
                "Freight":             [freight],
                "total_item_quantity": [total_item_quantity],
                "total_item_dollars":  [total_item_dollars]
            })

            scaled     = scaler.transform(df)
            prediction = flag_model.predict(scaled)[0]
            confidence = (
                max(flag_model.predict_proba(scaled)[0]) * 100
                if hasattr(flag_model, "predict_proba") else 95.0
            )
            conf_int = int(confidence)

            is_risk = prediction == 1
            card_cls     = "risk" if is_risk else "safe"
            tag_text     = "⚠ Risk Detected"    if is_risk else "✦ Analysis Complete"
            headline     = "HIGH RISK INVOICE"   if is_risk else "NORMAL INVOICE"
            desc         = ("This invoice exhibits anomalous patterns and has been flagged for manual review."
                            if is_risk else
                            "No anomalies detected. This invoice passes all risk thresholds.")
            fill_cls     = "conf-fill-risk"      if is_risk else "conf-fill-safe"

            st.markdown(f"""
            <div class="result-card {card_cls}">
                <div class="result-tag {card_cls}">{tag_text}</div>
                <div class="result-headline {card_cls}">{headline}</div>
                <div class="result-desc">{desc}</div>
                <div class="conf-label">
                    <span>Model Confidence</span>
                    <span style="color:#E8EDF5; font-weight:600">{confidence:.1f}%</span>
                </div>
                <div class="conf-track">
                    <div class="{fill_cls}" style="width:{conf_int}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Radar chart — cleaner labels
            display_labels = ["Qty", "Dollars", "Freight", "Total Qty", "Total $"]
            maxvals  = [500, 50000, 1000, 500, 50000]
            raw_vals = [invoice_quantity, invoice_dollars, freight,
                        total_item_quantity, total_item_dollars]
            norm_vals = [min(v / m * 100, 100) for v, m in zip(raw_vals, maxvals)]

            radar_color = "#FF5A5A" if is_risk else "#63CAB7"
            radar_fill  = "rgba(255,90,90,0.1)" if is_risk else "rgba(99,202,183,0.1)"

            radar = go.Figure(go.Scatterpolar(
                r=norm_vals + [norm_vals[0]],
                theta=display_labels + [display_labels[0]],
                fill="toself",
                fillcolor=radar_fill,
                line=dict(color=radar_color, width=2),
                marker=dict(color=radar_color, size=5)
            ))
            radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    angularaxis=dict(
                        tickfont=dict(family="DM Sans", color="#6B7A99", size=11),
                        linecolor="rgba(255,255,255,0.06)",
                        gridcolor="rgba(255,255,255,0.04)"
                    ),
                    radialaxis=dict(
                        tickfont=dict(family="DM Sans", color="#6B7A99", size=9),
                        gridcolor="rgba(255,255,255,0.05)",
                        linecolor="rgba(255,255,255,0.05)",
                        range=[0, 100],
                        tickvals=[25, 50, 75, 100],
                        ticktext=["25%","50%","75%","100%"]
                    )
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=270,
                margin=dict(t=20, b=20, l=50, r=50)
            )
            st.plotly_chart(radar, use_container_width=True)

            # Export
            result_df = df.copy()
            result_df["Risk_Label"]    = "High Risk" if is_risk else "Normal"
            result_df["Confidence_%"]  = round(confidence, 2)
            csv = result_df.to_csv(index=False)
            st.download_button(
                "↓  Export as CSV",
                csv,
                "invoice_analysis.csv",
                "text/csv"
            )

        else:
            st.markdown("""
            <div class="empty-state" style="height:320px;">
                <span style="font-size:32px; opacity:0.25;">◎</span>
                <span>Risk analysis will appear here</span>
            </div>
            """, unsafe_allow_html=True)
