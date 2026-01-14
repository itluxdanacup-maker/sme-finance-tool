import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="BizHealth CEO Dashboard", page_icon="💼", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .stNumberInput > div > div > input { text-align: right; font-weight: bold; }
    
    /* Card Styling */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value { font-size: 28px; font-weight: bold; color: #333; }
    .metric-label { font-size: 14px; color: #666; margin-bottom: 5px; }
    
    /* Pro Alert Box */
    .pro-alert {
        padding: 15px; border-radius: 8px; margin-bottom: 20px;
        border-left: 5px solid #007bff; background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR INPUT (COMPACT) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.markdown("### 💼 Executive Control")
    st.info("กรอกข้อมูลจริงเพื่อการวิเคราะห์ที่แม่นยำ")
    
    with st.expander("💰 สินทรัพย์ & เงินสด", expanded=True):
        cash = st.number_input("เงินสดในมือ (Cash)", 0, value=50000)
        receivables = st.number_input("ลูกหนี้การค้า (A/R)", 0, value=20000)
        inventory = st.number_input("มูลค่าสต็อก (Inventory)", 0, value=150000)

    with st.expander("📉 หนี้สิน & ค่าใช้จ่าย", expanded=True):
        debt = st.number_input("หนี้ระยะสั้น (Short-term Debt)", 0, value=40000)
        fixed_cost = st.number_input("Fixed Cost ต่อเดือน", 0, value=30000)
    
    with st.expander("📊 ผลประกอบการ", expanded=True):
        sales = st.number_input("ยอดขายเฉลี่ย (Sales)", 0, value=200000)
        cogs = st.number_input("ต้นทุนขาย (COGS)", 0, value=120000)
        ads = st.number_input("งบการตลาด (Ads)", 0, value=20000)

# --- 3. LOGIC ENGINE (THE BRAIN) ---
liquid_assets = cash + receivables
total_obligations = debt + fixed_cost
monthly_burn = fixed_cost + ads
net_profit = sales - cogs - monthly_burn

# Ratios
try:
    current_ratio = liquid_assets / debt if debt > 0 else 5
    runway = (liquid_assets - debt) / monthly_burn if monthly_burn > 0 else 12
    gross_margin = ((sales - cogs) / sales) * 100 if sales > 0 else 0
    net_margin = (net_profit / sales) * 100 if sales > 0 else 0
    inv_turnover = (cogs * 30) / inventory if inventory > 0 else 0 # Days to sell
except:
    current_ratio, runway, gross_margin, net_margin, inv_turnover = 0, 0, 0, 0, 0

# Benchmarking Score (เทียบกับมาตรฐานตลาดสมมติ)
# 0-5 Scale for Radar Chart
def get_score(val, target):
    score = (val / target) * 5
    return min(max(score, 0), 5)

score_liquidity = get_score(current_ratio, 1.5)
score_resilience = get_score(runway, 6)
score_margin = get_score(net_margin, 20)
score_efficiency = get_score(30/inv_turnover if inv_turnover > 0 else 0, 1) # ยิ่งน้อยยิ่งดี กลับเศษส่วน
score_growth = 3.5 # สมมติค่ากลางๆ

total_health_score = (score_liquidity + score_resilience + score_margin + score_efficiency)/4 * 20 # เต็ม 100

# --- 4. MAIN DASHBOARD ---
st.title("🛡️ BizHealth: CEO Dashboard")
st.markdown(f"**Status:** {'🟢 Healthy' if total_health_score > 70 else '🟡 Warning' if total_health_score > 40 else '🔴 Critical'} | **Score:** {total_health_score:.0f}/100")

# 4.1 TOP METRICS (STYLE แบบ DASHBOARD หรู)
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"""<div class="metric-card"><div class="metric-label">💰 Cash Runway</div><div class="metric-value" style="color:{'#28a745' if runway>3 else '#dc3545'}">{runway:.1f} Mo.</div></div>""", unsafe_allow_html=True)
c2.markdown(f"""<div class="metric-card"><div class="metric-label">📉 Net Profit</div><div class="metric-value" style="color:{'#28a745' if net_profit>0 else '#dc3545'}">{net_profit:,.0f}</div></div>""", unsafe_allow_html=True)
c3.markdown(f"""<div class="metric-card"><div class="metric-label">📊 Net Margin</div><div class="metric-value">{net_margin:.1f}%</div></div>""", unsafe_allow_html=True)
c4.markdown(f"""<div class="metric-card"><div class="metric-label">📦 Stock Health</div><div class="metric-value">{inventory/cogs*30:.0f} Days</div></div>""", unsafe_allow_html=True)

st.write("##")

# 4.2 ADVANCED CHARTS
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("🧪 Stress Test Simulation")
    st.caption("จำลองสถานการณ์: ธุรกิจคุณจะทนได้แค่ไหนถ้ายอดขายตก?")
    
    # Stress Test Logic
    drop_range = list(range(0, 101, 5))
    runway_projection = []
    
    breaking_point = None
    
    for drop in drop_range:
        sim_sales = sales * (1 - drop/100)
        sim_gross = sim_sales - (sim_sales * (cogs/sales)) if sales > 0 else 0 # COGS ลดตามยอดขาย
        sim_profit = sim_gross - monthly_burn
        
        # คำนวณเงินสดที่เหลือสะสม (Burn Rate ใหม่)
        # ถ้าขาดทุน คือกินเงินเก่า
        burn = abs(sim_profit) if sim_profit < 0 else 0
        months_survive = (liquid_assets - debt) / burn if burn > 0 else 99
        
        if months_survive > 24: months_survive = 24
        runway_projection.append(months_survive)
        
        if months_survive < 1 and breaking_point is None:
            breaking_point = drop

    # Area Chart สวยๆ
    fig_stress = go.Figure()
    fig_stress.add_trace(go.Scatter(
        x=drop_range, y=runway_projection, mode='lines', fill='tozeroy', 
        name='Survival Months', line=dict(color='#007bff', width=3)
    ))
    
    # Add Threshold Line
    fig_stress.add_hline(y=3, line_dash="dash", line_color="red", annotation_text="เขตอันตราย (ต่ำกว่า 3 เดือน)")
    
    fig_stress.update_layout(
        xaxis_title="ยอดขายลดลง (%)",
        yaxis_title="จำนวนเดือนที่อยู่รอด (Runway)",
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_stress, use_container_width=True)
    
    if breaking_point:
        st.error(f"🚨 **จุดตายธุรกิจ (Breaking Point):** ถ้ายอดขายตกเกิน **{breaking_point}%** คุณจะมีเงินสดหมุนเวียนไม่ถึง 1 เดือน!")
    else:
        st.success("🛡️ **Strong:** ธุรกิจคุณแข็งแกร่งมาก แม้ยอดขายตก 100% ก็ยังมีเงินเก็บพออยู่ได้เกิน 2 ปี")

with col_right:
    st.subheader("🕸️ Business 360° Scan")
    st.caption("เทียบฟอร์มธุรกิจคุณ vs ค่าเฉลี่ยอุตสาหกรรม")
    
    categories = ['สภาพคล่อง (Liquidity)', 'ความอึด (Resilience)', 'กำไร (Margin)', 'การหมุนของ (Efficiency)', 'หนี้สิน (Debt)']
    
    # Logic กลับด้าน Debt Score (หนี้น้อย = คะแนนเยอะ)
    debt_score = 5 - (get_score(debt, liquid_assets) if liquid_assets > 0 else 5)
    
    values = [score_liquidity, score_resilience, score_margin, score_efficiency, debt_score]
    
    fig_radar = go.Figure()
    
    # User Data
    fig_radar.add_trace(go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself',
      name='ธุรกิจของคุณ',
      line_color='#1f77b4'
    ))
    
    # Industry Benchmark (สมมติ)
    fig_radar.add_trace(go.Scatterpolar(
      r=[3, 3, 3, 3, 3],
      theta=categories,
      name='ค่าเฉลี่ยตลาด',
      line_color='#aaaaaa',
      line_dash='dot'
    ))

    fig_radar.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
      showlegend=True,
      height=350,
      margin=dict(l=40, r=40, t=20, b=20)
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 5. AUTOMATED EXECUTIVE REPORT ---
st.write("---")
st.subheader("📑 CEO Executive Summary")
st.markdown("""<div class="pro-alert">
    <b>💡 AI Analysis:</b> ระบบกำลังประมวลผลข้อมูลเพื่อสรุปคำแนะนำเชิงกลยุทธ์...
    </div>""", unsafe_allow_html=True)

report_col1, report_col2 = st.columns(2)

with report_col1:
    st.markdown("**1. สถานะทางการเงิน (Financial Health):**")
    if current_ratio < 1:
        st.write("🔴 **วิกฤต:** หนี้สินระยะสั้นสูงกว่าสินทรัพย์ที่มี ความเสี่ยงผิดนัดชำระหนี้สูงมาก")
    elif current_ratio < 1.5:
        st.write("🟡 **เฝ้าระวัง:** สภาพคล่องตึงตัว ควรชะลอการลงทุนและเน้นเก็บเงินสด")
    else:
        st.write("🟢 **แข็งแกร่ง:** สภาพคล่องสูง มีความพร้อมในการรับมือวิกฤตหรือขยายกิจการ")
        
    st.markdown("**2. ประสิทธิภาพการทำกำไร (Profitability):**")
    if net_margin < 5:
        st.write(f"🔴 **ต่ำ:** Net Margin {net_margin:.1f}% น้อยเกินไป เสี่ยงขาดทุนหากค่าแอดแพงขึ้น")
    elif net_margin < 15:
        st.write(f"🟡 **ปานกลาง:** Net Margin {net_margin:.1f}% อยู่ในเกณฑ์มาตรฐาน แต่ควรหาทางลดต้นทุน COGS")
    else:
        st.write(f"🟢 **สูง:** Net Margin {net_margin:.1f}% ทำได้ดีมาก แสดงถึง Brand Value ที่แข็งแรง")

with report_col2:
    st.markdown("**3. คำแนะนำเชิงกลยุทธ์ (Strategic Action):**")
    actions = []
    if runway < 3: actions.append("- ⚠️ **Urgent:** ต้องหาแหล่งเงินทุนเพิ่ม หรือระบายสต็อกเป็นเงินสดทันที")
    if inv_turnover > 90: actions.append("- 📦 **Stock Warning:** สินค้าหมุนเวียนช้าเกินไป (ติดดอย) ควรจัดโปรโมชั่นล้างสต็อก")
    if ads/sales > 0.3: actions.append("- 📢 **Ads Efficiency:** ค่าโฆษณาสูงเกิน 30% ของยอดขาย ควรปรับกลุ่มเป้าหมายหรือทำ Content ใหม่")
    if not actions: actions.append("- ✅ **Maintain:** รักษามาตรฐานปัจจุบัน และมองหาโอกาส Scale up ธุรกิจ")
    
    for action in actions:
        st.write(action)
