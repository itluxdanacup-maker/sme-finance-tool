import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SME Survival Kit Pro", page_icon="🚀", layout="wide")

# Custom CSS: เน้นความสวยงามและอ่านง่าย
st.markdown("""
<style>
    .big-metric { font-size: 30px !important; font-weight: bold; color: #333; }
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    .warning-text { color: #FFC107; font-weight: bold; }
    .danger-text { color: #FF5252; font-weight: bold; }
    .safe-text { color: #4CAF50; font-weight: bold; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🚀 SME Survival Kit: ระบบผ่าตัดธุรกิจออนไลน์")
st.markdown("**'รู้ตัวเลข = รอด'** | เครื่องมือวิเคราะห์สภาพคล่องและจำลองสถานการณ์จริง")
st.divider()

# --- 3. INPUT SIDEBAR (ละเอียดขึ้น) ---
with st.sidebar:
    st.header("📝 ข้อมูลธุรกิจของคุณ")
    
    with st.expander("1. กระเป๋าเงิน (Liquidity)", expanded=True):
        cash_on_hand = st.number_input("เงินสดในมือ/บัญชี (บาท)", 50000, step=1000)
        receivables = st.number_input("เงินรอเข้า (Platform/ลูกหนี้)", 20000, step=1000)
    
    with st.expander("2. ภาระหนี้สิน (Liabilities)", expanded=True):
        debt_supplier = st.number_input("หนี้ค่าของ (Supplier)", 30000, step=1000)
        debt_ads = st.number_input("หนี้ค่าโฆษณา (บัตรเครดิต)", 10000, step=1000)
        other_urgent_debt = st.number_input("หนี้อื่นที่ต้องจ่ายใน 30 วัน", 0, step=1000)
        
    with st.expander("3. โครงสร้างกำไร (Profit Structure)", expanded=True):
        avg_sales = st.number_input("ยอดขายเฉลี่ยต่อเดือน (บาท)", 150000, step=5000)
        cogs_percent = st.slider("ต้นทุนสินค้า (COGS) เป็นกี่ % ของยอดขาย?", 10, 90, 60)
        ads_percent = st.slider("ค่าโฆษณาปกติ เป็นกี่ % ของยอดขาย?", 1, 50, 20)
        fixed_cost = st.number_input("ค่าใช้จ่ายคงที่ (เงินเดือน/เช่า/น้ำไฟ)", 30000, step=1000)
        stock_value = st.number_input("มูลค่าสต็อกสินค้า (ราคาทุน)", 100000, step=5000)

# --- 4. CALCULATION ENGINE ---

# รวมยอด
total_liquid = cash_on_hand + receivables
total_debt_30d = debt_supplier + debt_ads + other_urgent_debt + fixed_cost # รวม Fix cost เดือนนี้ไปด้วยเลย
liquidity_gap = total_liquid - total_debt_30d

# คำนวณกำไร
monthly_cogs = avg_sales * (cogs_percent / 100)
monthly_ads = avg_sales * (ads_percent / 100)
gross_profit = avg_sales - monthly_cogs
net_profit = gross_profit - monthly_ads - fixed_cost

# อัตราส่วนทางการเงิน
burn_rate = fixed_cost + monthly_ads # เงินที่ไหลออกแน่ๆ ถ้าไม่ลดงบแอด
runway = total_liquid / burn_rate if burn_rate > 0 else 99
inventory_months = stock_value / monthly_cogs if monthly_cogs > 0 else 0

# Breakeven (จุดคุ้มทุน)
# สูตร: Sales = Fixed / (1 - (Variable% + Ads%))
variable_cost_ratio = (cogs_percent + ads_percent) / 100
try:
    breakeven_sales = fixed_cost / (1 - variable_cost_ratio)
except:
    breakeven_sales = 0 # กัน Error หารด้วย 0

# Scoring System (0-100)
score = 0
if liquidity_gap > 0: score += 40
else: score += 0 # ถ้าเงินขาด 0 คะแนนส่วนนี้

if runway > 3: score += 30
elif runway > 1: score += 15

if net_profit > 0: score += 30
elif net_profit > -10000: score += 10

# --- 5. TABS INTERFACE ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard ตรวจสุขภาพ", "🔮 Simulator จำลองอนาคต", "📉 จุดตายธุรกิจ (Breakeven)"])

# === TAB 1: DASHBOARD ===
with tab1:
    # Health Score Gauge
    col_score, col_advice = st.columns([1, 2])
    
    with col_score:
        st.write("### 🏥 Health Score")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "darkblue"},
                     'steps': [
                         {'range': [0, 40], 'color': "#ffcccb"},
                         {'range': [40, 70], 'color': "#fff3cd"},
                         {'range': [70, 100], 'color': "#d4edda"}],
                     'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 40}}))
        fig_gauge.update_layout(height=250, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col_advice:
        st.write("### 📢 ผลวินิจฉัย:")
        if score < 40:
            st.error(f"🚨 **อาการหนัก (ICU):** คุณขาดสภาพคล่อง {abs(liquidity_gap):,.0f} บาท! เดือนนี้เงินไม่พอจ่ายหนี้ เสี่ยงล้มละลายหากไม่หาเงินกู้หรือระบายของด่วน")
        elif score < 70:
            st.warning(f"⚠️ **อาการทรงตัว:** พออยู่ได้ แต่ห้ามสะดุด กำไรสุทธิเดือนนี้อยู่ที่ {net_profit:,.0f} บาท ถ้าขายตกนิดเดียวจะเข้าเนื้อทันที")
        else:
            st.success(f"✅ **สุขภาพดี:** ธุรกิจแข็งแกร่ง กำไร {net_profit:,.0f} บาท สภาพคล่องเหลือเฟือ ขยายกิจการได้เลย")
            
        st.info(f"**💡 รู้หรือไม่?** สต็อกของคุณต้องใช้เวลา **{inventory_months:.1f} เดือน** ถึงจะระบายหมด (ถ้านานกว่า 3 เดือน ระวังเงินจม!)")

    # Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 สภาพคล่องสุทธิ", f"{liquidity_gap:,.0f}", delta_color="normal" if liquidity_gap>0 else "inverse")
    c2.metric("🔥 เงินสดหมดใน (Runway)", f"{runway:.1f} เดือน", "ยิ่งเยอะยิ่งดี")
    c3.metric("📉 กำไรสุทธิ (Net Profit)", f"{net_profit:,.0f}", delta_color="normal" if net_profit>0 else "inverse")
    c4.metric("🎯 จุดคุ้มทุน (Breakeven)", f"{breakeven_sales:,.0f}", f"{(avg_sales-breakeven_sales):,.0f} (Gap)")

# === TAB 2: SIMULATOR (KILLER FEATURE) ===
with tab2:
    st.subheader("🔮 What-If Analysis: ลองปรับดู ถ้าเกิดเหตุการณ์นี้.. จะรอดไหม?")
    
    col_sim_input, col_sim_output = st.columns(2)
    
    with col_sim_input:
        st.markdown("##### 🎛️ ปรับปัจจัยเสี่ยง")
        sim_sales_drop = st.slider("📉 ถ้ายอดขายตก (%)", 0, 80, 0)
        sim_ads_increase = st.slider("📢 ถ้าค่าแอดแพงขึ้น (%)", 0, 100, 0)
        sim_pay_debt = st.checkbox("จ่ายหนี้ Supplier ทั้งหมดทันที?")
        
    with col_sim_output:
        # คำนวณสถานการณ์จำลอง
        sim_sales = avg_sales * ((100 - sim_sales_drop) / 100)
        sim_ads_cost = monthly_ads * ((100 + sim_ads_increase) / 100)
        
        sim_gross_profit = sim_sales - (sim_sales * (cogs_percent/100))
        sim_net_profit = sim_gross_profit - sim_ads_cost - fixed_cost
        
        sim_cash_out = fixed_cost + sim_ads_cost + (debt_supplier if sim_pay_debt else 0)
        sim_cash_remain = total_liquid - sim_cash_out
        
        st.markdown("##### 🏁 ผลลัพธ์การจำลอง")
        if sim_cash_remain < 0:
            st.error(f"💥 **เจ๊ง/เงินขาดมือ:** {sim_cash_remain:,.0f} บาท")
        else:
            st.success(f"🛡️ **รอด:** เหลือเงิน {sim_cash_remain:,.0f} บาท")
            
        st.metric("กำไรคาดการณ์ใหม่", f"{sim_net_profit:,.0f} บาท")
        
    # Graph Simulation
    labels = ['รายรับ (Sales)', 'ต้นทุนของ (COGS)', 'ค่าแอด (Ads)', 'Fix Cost', 'กำไร/ขาดทุน']
    values = [sim_sales, sim_sales*(cogs_percent/100), sim_ads_cost, fixed_cost, sim_net_profit]
    colors = ['blue', 'red', 'orange', 'gray', 'green' if sim_net_profit > 0 else 'red']
    
    fig_waterfall = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "relative", "relative", "total"],
        x = labels,
        textposition = "outside",
        text = [f"{v:,.0f}" for v in values],
        y = [sim_sales, -sim_sales*(cogs_percent/100), -sim_ads_cost, -fixed_cost, sim_net_profit],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    fig_waterfall.update_layout(title = "เส้นทางของเงินในสถานการณ์จำลอง", height=400)
    st.plotly_chart(fig_waterfall, use_container_width=True)

# === TAB 3: BREAKEVEN & STRATEGY ===
with tab3:
    st.subheader("🎯 เป้าหมายความอยู่รอด")
    
    col_be1, col_be2 = st.columns(2)
    
    with col_be1:
        st.markdown(f"""
        #### คุณต้องขายให้ได้เดือนละ:
        # 💰 {breakeven_sales:,.0f} บาท
        
        **(หรือประมาณ {breakeven_sales / (avg_sales/300):,.0f} ออเดอร์ หากคิดราคาเฉลี่ยเท่าเดิม)**
        """)
        
        current_progress = min((avg_sales / breakeven_sales), 1.5) if breakeven_sales > 0 else 0
        st.progress(min(current_progress/1.5, 1.0))
        
        if avg_sales > breakeven_sales:
            st.success(f"🎉 ตอนนี้คุณขายเกินจุดคุ้มทุนมา {avg_sales - breakeven_sales:,.0f} บาท (นี่คือกำไรเนื้อๆ)")
        else:
            st.error(f"⚠️ คุณยังขาดอีก {breakeven_sales - avg_sales:,.0f} บาท ถึงจะเริ่มมีกำไรบาทแรก")
            
    with col_be2:
        # Pie Chart โครงสร้างต้นทุน
        cost_data = {
            'ต้นทุนสินค้า': monthly_cogs,
            'ค่าโฆษณา': monthly_ads,
            'Fixed Cost': fixed_cost,
            'กำไร (Net)': max(net_profit, 0)
        }
        fig_pie = px.pie(values=list(cost_data.values()), names=list(cost_data.keys()), title='เงินขาย 100 บาท หายไปไหนบ้าง?')
        st.plotly_chart(fig_pie, use_container_width=True)
