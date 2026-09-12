import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# ---------------------------------------------------------
# 1. PAGE CONFIG & HIGH-END FINTECH STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="StockVerse Pro | Financial Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Body Background */
    .stApp {
        background: #080d1a;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #0d1527 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Sidebar Radio Options Styling */
    div[data-testid="stRadio"] > label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.3);
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        margin-bottom: 8px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(16, 185, 129, 0.1) !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        transform: translateX(4px);
    }

    /* Glassmorphism Header Box */
    .header-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.4) 100%);
        backdrop-filter: blur(16px);
        padding: 24px 28px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }

    /* Custom Animated Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 20px;
        border-radius: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(16, 185, 129, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 12px 28px -8px rgba(16, 185, 129, 0.25);
    }

    /* Custom Modern Table */
    table.custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 16px 0;
        font-size: 0.92rem;
        background-color: rgba(15, 23, 42, 0.5);
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    table.custom-table th {
        background-color: #0f172a;
        color: #38bdf8;
        text-align: left;
        padding: 16px;
        font-weight: 600;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    table.custom-table td {
        padding: 14px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        color: #e2e8f0;
        transition: background 0.2s ease;
    }

    table.custom-table tr:hover td {
        background-color: rgba(51, 65, 85, 0.3);
    }

    #MainMenu {visibility: visible;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SESSION STATE & DATA DICTIONARIES
# ---------------------------------------------------------
if "user_portfolio" not in st.session_state:
    st.session_state.user_portfolio = [
        {"Ticker": "NIFTYBEES.NS", "Name": "Nifty 50 ETF", "Buy Price": 250.0, "Qty": 30},
        {"Ticker": "BEL.NS", "Name": "Bharat Electronics", "Buy Price": 290.0, "Qty": 10},
        {"Ticker": "SUZLON.NS", "Name": "Suzlon Energy", "Buy Price": 55.0, "Qty": 40}
    ]

POPULAR_STOCKS_DICT = {
    "NIFTYBEES.NS": "Nifty 50 ETF",
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
    "TATAMOTORS.NS": "Tata Motors",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel",
    "BEL.NS": "Bharat Electronics",
    "SUZLON.NS": "Suzlon Energy",
    "ITC.NS": "ITC Limited",
    "Custom Ticker": "Custom Stock"
}

# ---------------------------------------------------------
# 3. SIDEBAR NAVIGATION WITH PRO ICONS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 12px 0 20px 0;">
            <h2 style="color: #10b981; margin: 0; font-size: 1.6rem; letter-spacing: -0.5px;">💎 StockVerse <span style="font-size:0.7rem; background:#10b98122; color:#10b981; padding:2px 8px; border-radius:12px; border:1px solid #10b98144;">PRO</span></h2>
            <p style="color: #64748b; font-size: 0.8rem; margin-top: 6px;">Modern Portfolio Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    selected_page = st.radio(
        "Navigation Module",
        options=[
            "📊  Market Dashboard", 
            "💼  Portfolio Tracker", 
            "🍕  Capital Allocation",
            "📈  Trend Analyzer", 
            "🧮  Return Estimator"
        ]
    )
    
    st.markdown("---")
    st.markdown("""
        <div style="padding: 12px; background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.15); border-radius: 12px; text-align: center;">
            <span style="color: #10b981; font-size: 0.8rem; font-weight: 600;">● Live NSE Feed Active</span>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. DYNAMIC HEADER BANNER
# ---------------------------------------------------------
st.markdown(f"""
    <div class="header-box">
        <h2 style="color: #10b981; margin:0; font-size: 1.8rem; letter-spacing: -0.5px;">StockVerse Terminal</h2>
        <p style="color: #94a3b8; margin-top: 6px; font-size: 0.9rem;">
            Active View: <b style="color: #38bdf8;">{selected_page}</b>
        </p>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# MODULE 1: MARKET DASHBOARD
# =========================================================
if selected_page == "📊  Market Dashboard":
    st.subheader("🌐 Indian Market Benchmarks")
    st.caption("Real-time index updates")

    indices = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANK NIFTY": "^NSEBANK",
        "NIFTY IT": "^CNXIT"
    }

    ind_cols = st.columns(len(indices))
    for idx, (name, symbol) in enumerate(indices.items()):
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                curr = float(hist['Close'].iloc[-1])
                prev = float(hist['Close'].iloc[-2])
                chg = curr - prev
                chg_pct = (chg / prev) * 100
            elif len(hist) == 1:
                curr = float(hist['Close'].iloc[-1])
                chg, chg_pct = 0.0, 0.0
            else:
                curr, chg, chg_pct = 0.0, 0.0, 0.0
            
            with ind_cols[idx]:
                st.metric(
                    label=name,
                    value=f"₹{curr:,.2f}",
                    delta=f"{chg:,.2f} ({chg_pct:.2f}%)"
                )
        except Exception:
            with ind_cols[idx]:
                st.metric(label=name, value="Unavailable")

    st.markdown("---")
    st.subheader("🔥 Key Watchlist Stocks")

    watchlist_tickers = [
        ("RELIANCE.NS", "Reliance Industries"),
        ("TCS.NS", "Tata Consultancy Services"),
        ("HDFCBANK.NS", "HDFC Bank"),
        ("INFY.NS", "Infosys"),
        ("TATAMOTORS.NS", "Tata Motors"),
        ("ICICIBANK.NS", "ICICI Bank"),
        ("SBIN.NS", "State Bank of India"),
        ("BHARTIARTL.NS", "Bharti Airtel")
    ]

    market_rows = ""
    with st.spinner("Syncing Watchlist market data..."):
        for symbol, name in watchlist_tickers:
            try:
                t = yf.Ticker(symbol)
                hist = t.history(period="2d")
                if not hist.empty:
                    curr = float(hist['Close'].iloc[-1])
                    prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else curr
                    chg = curr - prev
                    chg_pct = (chg / prev) * 100
                    
                    color = "#10b981" if chg >= 0 else "#f43f5e"
                    market_rows += f"""
                    <tr>
                        <td><b>{name}</b></td>
                        <td><span style="color: #64748b; font-family: monospace;">{symbol}</span></td>
                        <td>₹{curr:,.2f}</td>
                        <td style="color:{color}; font-weight:600;">{chg:+,.2f}</td>
                        <td style="color:{color}; font-weight:600;">{chg_pct:+.2f}%</td>
                    </tr>
                    """
            except Exception:
                pass

    if market_rows:
        html_table = f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Company Name</th>
                    <th>Ticker</th>
                    <th>Price (₹)</th>
                    <th>Change (₹)</th>
                    <th>Change (%)</th>
                </tr>
            </thead>
            <tbody>
                {market_rows}
            </tbody>
        </table>
        """
        st.markdown(html_table, unsafe_allow_html=True)

# =========================================================
# MODULE 2: PORTFOLIO TRACKER
# =========================================================
elif selected_page == "💼  Portfolio Tracker":
    st.subheader("💼 Holdings & P&L Manager")
    
    with st.expander("➕ Add New Holdings", expanded=False):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            selected_stock_option = st.selectbox(
                "Choose Asset:",
                options=list(POPULAR_STOCKS_DICT.keys()),
                format_func=lambda x: f"{POPULAR_STOCKS_DICT[x]} ({x})" if x != "Custom Ticker" else "➕ Custom Ticker Input"
            )
            
            if selected_stock_option == "Custom Ticker":
                new_ticker = st.text_input("NSE Symbol (e.g. ITC.NS):").upper()
            else:
                new_ticker = selected_stock_option

        with col_f2:
            if selected_stock_option != "Custom Ticker":
                default_name = POPULAR_STOCKS_DICT[selected_stock_option]
                new_name = st.text_input("Name:", value=default_name)
            else:
                new_name = st.text_input("Name:")

        with col_f3:
            new_price = st.number_input("Average Price (₹):", min_value=0.1, value=100.0, step=1.0)
        with col_f4:
            new_qty = st.number_input("Quantity:", min_value=1, value=10, step=1)
        
        if st.button("Add Position"):
            if new_ticker and new_name:
                st.session_state.user_portfolio.append({
                    "Ticker": new_ticker,
                    "Name": new_name,
                    "Buy Price": float(new_price),
                    "Qty": int(new_qty)
                })
                st.success(f"Added {new_name} to portfolio!")
                st.rerun()

    st.markdown("---")
    st.subheader("📊 Portfolio Valuation")

    total_invested = 0.0
    total_current_val = 0.0

    if st.session_state.user_portfolio:
        cols = st.columns(min(len(st.session_state.user_portfolio), 4))
        
        for idx, item in enumerate(st.session_state.user_portfolio):
            ticker_symbol = item["Ticker"]
            buy_price = float(item["Buy Price"])
            qty = int(item["Qty"])
            invested = buy_price * qty

            try:
                t = yf.Ticker(ticker_symbol)
                hist = t.history(period="1d")
                current_price = float(hist['Close'].iloc[-1]) if not hist.empty else buy_price
            except Exception:
                current_price = buy_price

            current_val = current_price * qty
            pnl = current_val - invested
            pnl_pct = (pnl / invested) * 100 if invested > 0 else 0.0

            total_invested += invested
            total_current_val += current_val

            col_target = cols[idx % 4]
            with col_target:
                st.metric(
                    label=f"{item['Name']} ({ticker_symbol})",
                    value=f"₹{current_val:,.2f}",
                    delta=f"₹{pnl:,.2f} ({pnl_pct:.2f}%)"
                )

        net_pnl = total_current_val - total_invested
        net_pnl_pct = (net_pnl / total_invested) * 100 if total_invested > 0 else 0.0

        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Capital Invested", f"₹{total_invested:,.2f}")
        m2.metric("Portfolio Valuation", f"₹{total_current_val:,.2f}")
        m3.metric("Net Gain / Loss", f"₹{net_pnl:,.2f}", delta=f"{net_pnl_pct:.2f}%")

# =========================================================
# MODULE 3: CAPITAL ALLOCATION
# =========================================================
elif selected_page == "🍕  Capital Allocation":
    st.subheader("🍕 Portfolio Distribution")
    
    if st.session_state.user_portfolio:
        try:
            pie_names = []
            pie_vals = []
            for item in st.session_state.user_portfolio:
                try:
                    t = yf.Ticker(item["Ticker"])
                    hist = t.history(period="1d")
                    cp = float(hist['Close'].iloc[-1]) if not hist.empty else item["Buy Price"]
                except Exception:
                    cp = item["Buy Price"]
                
                pie_names.append(item["Name"])
                pie_vals.append(cp * item["Qty"])

            fig_pie = px.pie(
                names=pie_names, 
                values=pie_vals, 
                title='Capital Distribution Ratio',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Emerald
            )
            fig_pie.update_layout(
                template="plotly_dark",
                paper_bgcolor='#080d1a',
                plot_bgcolor='#080d1a',
                font=dict(color="#e2e8f0", family="Plus Jakarta Sans")
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        except Exception:
            st.error("Unable to render portfolio chart.")

# =========================================================
# MODULE 4: TREND ANALYZER
# =========================================================
elif selected_page == "📈  Trend Analyzer":
    st.subheader("📈 Smooth Price Trend Visualizer")
    st.caption("Clutter-free market trend curves")
    
    screener_choice = st.selectbox(
        "Select Asset:",
        options=list(POPULAR_STOCKS_DICT.keys()),
        format_func=lambda x: f"{POPULAR_STOCKS_DICT[x]} ({x})" if x != "Custom Ticker" else "✏️ Custom Manual Search"
    )

    if screener_choice == "Custom Ticker":
        user_ticker = st.text_input("Enter NSE Ticker Symbol:", value="NIFTYBEES.NS").upper()
    else:
        user_ticker = screener_choice

    if user_ticker:
        try:
            stock = yf.Ticker(user_ticker)
            df_stock = stock.history(period="6mo")

            if not df_stock.empty:
                curr_p = float(df_stock['Close'].iloc[-1])
                prev_p = float(df_stock['Close'].iloc[-2]) if len(df_stock) > 1 else curr_p
                chg = curr_p - prev_p
                chg_pct = (chg / prev_p) * 100 if prev_p > 0 else 0.0

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Current Price", f"₹{curr_p:,.2f}", f"{chg:+,.2f} ({chg_pct:+.2f}%)")
                c2.metric("Highest (6M)", f"₹{float(df_stock['High'].max()):,.2f}")
                c3.metric("Lowest (6M)", f"₹{float(df_stock['Low'].min()):,.2f}")
                c4.metric("Average Price", f"₹{float(df_stock['Close'].mean()):,.2f}")

                st.markdown("---")
                st.markdown(f"#### 📊 Price Trend Curve — **{user_ticker}**")

                fig_line = px.area(
                    df_stock, 
                    x=df_stock.index, 
                    y="Close",
                    labels={'Close': 'Price (₹)', 'Date': 'Timeline'},
                    title=f"6-Month Trend Curve ({user_ticker})"
                )

                line_color = "#10b981" if chg >= 0 else "#f43f5e"
                fill_color = "rgba(16, 185, 129, 0.12)" if chg >= 0 else "rgba(244, 63, 94, 0.12)"

                fig_line.update_traces(
                    line_color=line_color,
                    fillcolor=fill_color
                )

                fig_line.update_layout(
                    template="plotly_dark",
                    height=420,
                    paper_bgcolor='#080d1a',
                    plot_bgcolor='#080d1a',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)')
                )

                st.plotly_chart(fig_line, use_container_width=True)

            else:
                st.warning("No data found for the selected symbol.")
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")

# =========================================================
# MODULE 5: RETURN ESTIMATOR
# =========================================================
elif selected_page == "🧮  Return Estimator":
    st.subheader("🧮 Tax & Wealth Growth Estimator")
    
    st.markdown("#### 1. CNC Delivery Taxes")
    trade_val = st.number_input("Total Trade Turnover (Buy + Sell Value in ₹):", value=10000.0, step=1000.0)
    
    stt = trade_val * 0.001
    exchange_charges = trade_val * 0.000345
    gst = exchange_charges * 0.18
    sebi_fee = (trade_val / 10000000.0) * 10.0
    total_tax = stt + exchange_charges + gst + sebi_fee

    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("STT Tax", f"₹{stt:.2f}")
    tc2.metric("Exchange & GST", f"₹{(exchange_charges + gst):.2f}")
    tc3.metric("Total Tax & Fees", f"₹{total_tax:.2f}")

    st.markdown("---")
    st.markdown("#### 2. CAGR Return Forecast")

    BENCHMARK_PRESETS = {
        "NIFTY 50 Index Fund": {"cagr": 13.0, "name": "NIFTY 50 Benchmark"},
        "SENSEX Index": {"cagr": 12.5, "name": "BSE SENSEX"},
        "NIFTY IT Sector": {"cagr": 15.0, "name": "NIFTY IT Index"},
        "Gold ETF": {"cagr": 10.0, "name": "Gold BeES"},
        "Nifty Midcap 100": {"cagr": 16.5, "name": "Midcap Index"},
        "Custom Asset": {"cagr": 12.0, "name": "Custom Asset"}
    }

    col_u1, col_u2, col_u3, col_u4 = st.columns(4)
    
    with col_u1:
        preset_choice = st.selectbox("Asset Preset:", options=list(BENCHMARK_PRESETS.keys()))
        asset_name = BENCHMARK_PRESETS[preset_choice]["name"]
    
    with col_u2:
        invest_amount = st.number_input("Investment (₹):", value=10000, step=1000)
    
    with col_u3:
        default_cagr = BENCHMARK_PRESETS[preset_choice]["cagr"]
        custom_cagr = st.number_input("CAGR Rate (%):", value=default_cagr, step=0.5)
    
    with col_u4:
        duration_years = st.slider("Duration (Years):", min_value=1, max_value=20, value=5)

    r_decimal = custom_cagr / 100.0
    future_est_val = invest_amount * ((1 + r_decimal) ** duration_years)
    net_profit_est = future_est_val - invest_amount
    total_pct_return = (net_profit_est / invest_amount) * 100 if invest_amount > 0 else 0.0

    st.markdown(f"##### 🎯 Projected Forecast for **{asset_name}** (@ {custom_cagr}% CAGR)")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("Principal Capital", f"₹{invest_amount:,.2f}")
    res_c2.metric(f"Maturity Value ({duration_years} Yrs)", f"₹{future_est_val:,.2f}")
    res_c3.metric("Projected Wealth Profit", f"₹{net_profit_est:,.2f}", delta=f"+{total_pct_return:.1f}%")

st.markdown("---")
st.caption("💎 StockVerse Engine • High-End Financial Intelligence Suite")