import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. SETUP & STYLE ---
st.set_page_config(page_title="SME Health Check", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    /* ปรับ UI ให้สะอาดตา เหมือน App มือถือ */
    .block-container { padding-top: 2rem; }
    .stNumberInput > div > div > input { text-align: right; }
    .big-font { font-size: 20px !important; color: #555; }
    .result-card { padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .safe { background-color: #d1e7dd; color: #0f5132; border-left: 5px solid #198754; }
    .warning { background-color: #fff3cd; color: #664d03; border-left: 5px solid #ffc107; }
    .danger { background-color: #f8d7da; color: #842029; border-left: 5px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

# --- 2. INPUT SECTION (SIMPLE FRONTEND) ---
st.title("🏥 ตรวจสุขภาพธุรกิจ (ฉบับใช้งานจริง)")
st.caption("กรอกตัวเลขจริงของเดือนนี้ (ใส่ 0 ได้ถ้าไม่มี)")

col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    st.subheader("1. เงินสด & ทรัพย์สิน")
    cash = st.number_input("เงินสดในมือ/ธนาคาร", min_value=0, value=0, help="เงินที่ดึงมาใช้ได้ทันที")
    receivables = st.number_input("ลูกหนี้การค้า/เงินรอโอน", min_value=0, value=0, help="เงินจากลูกค้า หรือ Platform ที่กำลังจะโอนมา")
    inventory = st.number_input("มูลค่าสต็อกสินค้า (ราคาทุน)", min_value=0, value=0)

with col_input2:
    st.subheader("2. หนี้สิน & รายจ่าย")
    short_term_debt = st.number_input("หนี้ต้องจ่ายใน 30 วัน", min_value=0, value=0, help="ค่าของ, ค่าแอด, บัตรเครดิต")
    fixed_cost = st.number_input("รายจ่ายคงที่ต่อเดือน", min_value=0, value=0, help="ค่าเช่า, เงินเดือน, ค่าน้ำไฟ")
    
with col_input3:
    st.subheader("3. ผลประกอบการ")
    monthly_sales = st.number_input("ยอดขายเฉลี่ยต่อเดือน", min_value=0, value=0)
    cogs = st.number_input("ต้นทุนสินค้าขาย (COGS)", min_value=0, value=0, help="เฉพาะค่าต้นทุนของสินค้าที่ขายไป")
    ads_cost = st.number_input("ค่าโฆษณา/การตลาด", min_value=0, value=0)

st.divider()

# --- 3. COMPLEX BACKEND LOGIC (The Brain) ---
# ระบบคำนวณหลังบ้านที่ซับซ้อนขึ้น เพื่อความแม่นยำ

# ตัวแปรคำนวณพื้นฐาน
total_liquid_assets = cash + receivables
total_obligations = short_term_debt + fixed_cost
net_burn_rate = fixed_cost + ads_cost
gross_profit = monthly_sales - cogs
net_profit = gross_profit - net_burn_rate

# ป้องกัน Error หารด้วยศูนย์ (Division by Zero Protection)
def safe_div(n, d):
    return n / d if d > 0 else 0

# 3.1 Advanced Ratios
# Cash Runway (อยู่ได้กี่เดือน) - คิดละเอียดรวมหนี้ระยะสั้น
runway_months = safe_div(total_liquid_assets - short_term_debt, net_burn_rate) 
if runway_months < 0: runway_months = 0 # ถ้าติดลบคืออยู่ไม่ได้เลย

# Defensive Interval Ratio (DIR) - ธุรกิจอยู่ได้กี่วันถ้าไม่มีรายได้เข้าเลย
daily_burn = net_burn_rate / 30
dir_days = safe_div(total_liquid_assets, daily_burn)

# Quick Ratio (สภาพคล่องหมุนเร็ว)
quick_ratio = safe_div(total_liquid_assets, short_term_debt) if short_term_debt > 0 else 99

# Inventory Turnover Days (ของจมกี่วัน)
inventory_days = safe_div(inventory, (cogs / 30))

# 3.2 Scoring Algorithm (Weighted Score)
# ให้คะแนนเต็ม 100 โดยถ่วงน้ำหนักปัจจัยสำคัญ
score = 0
# Factor 1: Liquidity (40%)
if quick_ratio >= 1.0: score += 40
elif quick_ratio >= 0.8: score += 20
elif quick_ratio >= 0.5: score += 10

# Factor 2: Runway (30%)
if runway_months >= 6: score += 30
elif runway_months >= 3: score += 20
elif runway_months >= 1: score += 10

# Factor 3: Profitability (30%)
profit_margin = safe_div(net_profit, monthly_sales)
if profit_margin > 0.15: score += 30 # กำไร > 15%
elif profit_margin > 0: score += 15  # มีกำไรนิดหน่อย
elif profit_margin > -0.1: score += 5 # ขาดทุนไม่เยอะ

# --- 4. OUTPUT DISPLAY (SIMPLE FRONTEND) ---

# Logic เลือกสีและการแสดงผล
if score >= 80:
    status_color = "safe"
    status_icon = "✅"
    status_text = "แข็งแรงมาก"
    advice = "สภาพคล่องเหลือเฟือ ธุรกิจมีกำไร พร้อมสำหรับการขยายกิจการ หรือลงทุนเพิ่ม"
elif score >= 50:
    status_color = "warning"
    status_icon = "⚠️"
    status_text = "พอใช้ได้ (เฝ้าระวัง)"
    advice = "ธุรกิจเดินต่อได้แต่ห้ามสะดุด! ระวังอย่าสต็อกของเพิ่มเกินความจำเป็น และพยายามเก็บเงินสดเพิ่ม"
else:
    status_color = "danger"
    status_icon = "🚨"
    status_text = "อาการน่าเป็นห่วง (ICU)"
    advice = f"วิกฤต! เงินสดไม่พอหมุน คุณมีโอกาสเงินขาดมือในอีก {runway_months:.1f} เดือนข้างหน้า ต้องรีบระบายของหรือลดรายจ่ายด่วนที่สุด"

# แสดงผลแบบ Card ใหญ่ๆ เข้าใจง่าย
col_res1, col_res2 = st.columns([2, 1])

with col_res1:
    st.markdown(f"""
    <div class="result-card {status_color}">
        <h2 style='margin:0'>{status_icon} ผลวินิจฉัย: {status_text} (คะแนน {score}/100)</h2>
        <p class="big-font" style='margin-top:10px'>{advice}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 เงินสดสุทธิ (หลังหักหนี้)", f"{total_liquid_assets - short_term_debt:,.0f}", help="เงินสด + ลูกหนี้ - หนี้ที่ต้องจ่าย")
    m2.metric("📉 กำไร/ขาดทุน เดือนนี้", f"{net_profit:,.0f}", delta_color="normal")
    m3.metric("⏳ อยู่รอดได้อีก (Runway)", f"{runway_months:.1f} เดือน")

with col_res2:
    # Gauge Chart (ดูง่ายๆ)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Health Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#333"},
            'steps': [
                {'range': [0, 50], 'color': "#ffcccb"},
                {'range': [50, 80], 'color': "#fff3cd"},
                {'range': [80, 100], 'color': "#d1e7dd"}]
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20,r=20,t=30,b=20))
    st.plotly_chart(fig, use_container_width=True)

# --- 5. DEEP DIVE (กดเพื่อดูไส้ใน) ---
with st.expander("🔍 ดูรายละเอียดลึกๆ (สำหรับคนอยากรู้วิเคราะห์)"):
    st.write(f"**1. Defensive Interval Ratio:** {dir_days:.0f} วัน (ถ้าหยุดขายวันนี้ คุณจะอยู่ได้กี่วัน)")
    st.write(f"**2. Inventory Days:** {inventory_days:.0f} วัน (กว่าจะขายของสต็อกเดิมหมด ใช้เวลากี่วัน)")
    st.write(f"**3. Quick Ratio:** {quick_ratio:.2f} เท่า (สินทรัพย์สภาพคล่องสูง หารด้วย หนี้ระยะสั้น -- ควรมากกว่า 1.0)")
    
    if monthly_sales > 0:
        breakeven = net_burn_rate / ((monthly_sales - cogs) / monthly_sales)
        st.write(f"**4. จุดคุ้มทุน (Breakeven Sales):** ต้องมียอดขาย {breakeven:,.0f} บาท ถึงจะไม่ขาดทุน")
