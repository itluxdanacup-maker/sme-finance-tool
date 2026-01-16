import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Seller Super App", page_icon="🛍️", layout="centered")

st.markdown("""
<style>
    /* Styling ให้เหมือน App มือถือ */
    .big-stat { font-size: 32px !important; font-weight: bold; color: #333; text-align: center; }
    .success-text { color: #28a745; font-weight: bold; }
    .danger-text { color: #dc3545; font-weight: bold; }
    .card { background-color: #f7f9fc; padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #eef; }
    
    /* ปรับแต่ง Sidebar */
    section[data-testid="stSidebar"] { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=80)
    st.title("เมนูหลัก")
    menu = st.radio("เลือกเครื่องมือ:", 
        ["🛡️ คิดราคาขาย (Profit)", 
         "📢 ตรวจค่าแอด (Ads Doctor)", 
         "🏥 ตรวจสุขภาพร้าน (Cash Flow)"])
    
    st.markdown("---")
    st.caption("Version 2.0 (All-in-One)")

# ==========================================
# PAGE 1: 🛡️ PROFIT SHIELD (คิดราคา & กำไร)
# ==========================================
if menu == "🛡️ คิดราคาขาย (Profit)":
    st.title("🛡️ เครื่องคิดเลขกันเจ๊ง")
    st.caption("ขายราคานี้...เหลือเงินกี่บาท?")

    with st.container():
        # Input Section
        c1, c2 = st.columns(2)
        selling_price = c1.number_input("ราคาขาย (บาท)", 0.0, value=1590.0, step=10.0)
        cost_price = c2.number_input("ต้นทุนของ (รวมแพ็ค)", 0.0, value=650.0, step=10.0)
        
        c3, c4 = st.columns(2)
        gp_fee = c3.number_input("ค่าธรรมเนียม Platform (%)", 0.0, value=12.0, help="Shopee/Lazada/TikTok")
        ads_per_order = c4.number_input("ค่าแอดต่อบ้าน (บาท)", 0.0, value=250.0)
        
        has_vat = st.checkbox("จด VAT 7% (คิดภาษีขาย)", value=True)

    # Calculation Logic
    if selling_price > 0:
        # 1. ถอด VAT (ถ้ามี)
        net_selling_price = selling_price * 100 / 107 if has_vat else selling_price
        vat_amt = selling_price - net_selling_price
        
        # 2. Fee (คิดจากยอดเต็ม)
        fee_amt = selling_price * (gp_fee / 100)
        
        # 3. Total Cost
        total_deduct = cost_price + fee_amt + ads_per_order + vat_amt
        net_profit = selling_price - total_deduct
        margin_percent = (net_profit / selling_price) * 100

        # Output Display
        st.markdown("---")
        if net_profit > 0:
            st.markdown(f"<div class='big-stat success-text'>+{net_profit:,.0f} บาท</div>", unsafe_allow_html=True)
            st.caption(f"กำไรสุทธิ {margin_percent:.1f}% (เข้ากระเป๋าจริง)")
        else:
            st.markdown(f"<div class='big-stat danger-text'>{net_profit:,.0f} บาท</div>", unsafe_allow_html=True)
            st.error("🚨 ขาดทุน! ห้ามขายราคานี้เด็ดขาด")
            
        # Breakdown
        with st.expander("🔍 ดูไส้ใน (เงินหายไปไหน?)"):
            df = pd.DataFrame({
                "รายการ": ["ราคาขาย", "ต้นทุนของ", "ค่าธรรมเนียม", "ค่าแอด", "ภาษี (VAT)", "กำไรเหลือจริง"],
                "บาท": [selling_price, -cost_price, -fee_amt, -ads_per_order, -vat_amt, net_profit]
            })
            st.dataframe(df.style.format({"บาท": "{:,.2f}"}), hide_index=True)

# ==========================================
# PAGE 2: 📢 ADS DOCTOR (วิเคราะห์ค่าโฆษณา)
# ==========================================
elif menu == "📢 ตรวจค่าแอด (Ads Doctor)":
    st.title("📢 หมอตรวจแอด")
    st.caption("ยิงแอดไป คุ้มหรือไม่คุ้ม? ระบบช่วยคำนวณให้")
    
    col_a1, col_a2 = st.columns(2)
    ad_spend = col_a1.number_input("งบที่ใช้ไป (Ad Spend)", 0.0, value=5000.0)
    sales_from_ads = col_a2.number_input("ยอดขายที่ได้ (Sales)", 0.0, value=15000.0)
    
    profit_margin_percent = st.slider("กำไรขั้นต้นสินค้า (%)", 10, 90, 40, help="กำไรหลังหักต้นทุนของ (ไม่รวมค่าแอด)")

    st.markdown("---")
    
    # Logic
    if ad_spend > 0 and sales_from_ads > 0:
        # 1. Actual ROAS (Return on Ad Spend)
        actual_roas = sales_from_ads / ad_spend
        
        # 2. Break-even ROAS (จุดเท่าทุน)
        # สูตร: 1 / Profit Margin % 
        # เช่น กำไร 40% (0.4) -> 1/0.4 = 2.5 (ต้องได้ ROAS 2.5 ถึงจะเท่าทุน)
        breakeven_roas = 1 / (profit_margin_percent / 100)
        
        # 3. Profit/Loss Analysis
        gross_profit = sales_from_ads * (profit_margin_percent / 100)
        net_ads_profit = gross_profit - ad_spend
        
        # Display Result
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.metric("ROAS ที่ทำได้จริง", f"{actual_roas:.2f} เท่า")
        with c_res2:
            st.metric("ROAS ขั้นต่ำที่ต้องได้", f"{breakeven_roas:.2f} เท่า", 
                      help="ถ้าน้อยกว่าเลขนี้ คือขาดทุน")
        
        if actual_roas >= breakeven_roas:
            st.success(f"✅ **กำไร!** แอดตัวนี้ทำเงินได้ {net_ads_profit:,.0f} บาท (Scale ต่อได้)")
            st.balloons()
        else:
            st.error(f"❌ **ขาดทุน!** เสียเงินฟรี {abs(net_ads_profit):,.0f} บาท (ปิดแอดด่วน)")
            st.progress(min(actual_roas/breakeven_roas, 1.0))
            st.caption(f"ประสิทธิภาพทำได้แค่ {(actual_roas/breakeven_roas)*100:.0f}% ของจุดคุ้มทุน")

# ==========================================
# PAGE 3: 🏥 HEALTH CHECK (สภาพคล่อง)
# ==========================================
elif menu == "🏥 ตรวจสุขภาพร้าน (Cash Flow)":
    st.title("🏥 ตรวจสุขภาพการเงิน")
    
    with st.container():
        c_h1, c_h2, c_h3 = st.columns(3)
        cash = c_h1.number_input("เงินสดที่มี", 0, value=50000)
        debt = c_h2.number_input("หนี้ต้องจ่าย (30วัน)", 0, value=30000)
        expense = c_h3.number_input("รายจ่ายคงที่/เดือน", 0, value=20000)
    
    # Logic
    liquidity = cash - debt
    burn_rate = expense
    runway = (cash - debt) / burn_rate if burn_rate > 0 else 99
    
    st.markdown("### 📋 ผลการตรวจ")
    
    # Cards Design
    col_card1, col_card2 = st.columns(2)
    
    with col_card1:
        status_color = "#d4edda" if liquidity > 0 else "#f8d7da"
        st.markdown(f"""
        <div style="background-color:{status_color}; padding:15px; border-radius:10px;">
            <h4>💰 เงินหมุนเวียนสุทธิ</h4>
            <h2>{liquidity:,.0f} บาท</h2>
            <small>{'✅ พอใช้หนี้' if liquidity > 0 else '❌ ไม่พอจ่ายหนี้'}</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col_card2:
        runway_color = "#fff3cd"
        if runway < 1: runway_color = "#f8d7da"
        if runway > 3: runway_color = "#d4edda"
        
        st.markdown(f"""
        <div style="background-color:{runway_color}; padding:15px; border-radius:10px;">
            <h4>⏳ สายป่านธุรกิจ (Runway)</h4>
            <h2>{runway:.1f} เดือน</h2>
            <small>{'อยู่ได้ยาวๆ' if runway > 3 else 'เสี่ยงเจ๊งเร็วๆนี้'}</small>
        </div>
        """, unsafe_allow_html=True)
