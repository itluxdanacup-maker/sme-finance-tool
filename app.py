import streamlit as st
import pandas as pd
import math

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Seller Super App V5", page_icon="🛍️", layout="centered")

st.markdown("""
<style>
    .big-stat { font-size: 28px !important; font-weight: bold; color: #333; text-align: center; }
    .target-box { background-color: #e0f7fa; padding: 20px; border-radius: 15px; border: 2px solid #00bcd4; text-align: center; margin-bottom: 20px;}
    .daily-mission { font-size: 42px !important; font-weight: bold; color: #0097a7; }
    .helper-box { background-color: #fff3cd; padding: 15px; border-radius: 10px; border: 1px dashed #ffc107; margin-bottom: 15px; font-size: 14px;}
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURATION ---
PLATFORM_FEES = {
    "Facebook (โอนเอง/COD)": 0.0,
    "TikTok Shop": 8.0,
    "Shopee (Non-Mall)": 12.0,
    "Lazada (General)": 12.0,
    "LINE SHOPPING": 3.0
}

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=80)
    st.title("ระบบจัดการร้าน V5")
    menu = st.radio("เลือกเมนู:", 
        ["🎯 ตั้งเป้าหมาย (Mission)",
         "🛡️ คิดราคาขาย (Auto Price)", 
         "📢 ตรวจค่าแอด (Ads Doctor)", 
         "🏥 ตรวจสุขภาพร้าน (Cash Flow)"])
    st.caption("Facebook Friendly Mode")

# ==========================================
# PAGE 1: 🎯 MISSION CONTROL
# ==========================================
if menu == "🎯 ตั้งเป้าหมาย (Mission)":
    st.title("🎯 Mission Commander")
    st.caption("ตั้งเป้าหมายกำไร -> ระบบบอกงานรายวัน")

    target_profit = st.number_input("อยากได้กำไรเข้ากระเป๋าเดือนนี้ (บาท)", 0, value=100000, step=5000)
    st.markdown("---")
    
    # 1. PLATFORM
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        selected_platform = st.selectbox("ขายที่ไหน?", list(PLATFORM_FEES.keys()), index=0) # Default Facebook
    with col_p2:
        default_fee = PLATFORM_FEES[selected_platform]
        fee_percent = st.number_input(f"ค่าธรรมเนียม (%)", 0.0, value=default_fee)

    # 2. PRICE & COST
    c1, c2 = st.columns(2)
    avg_price = c1.number_input("ราคาขายเฉลี่ย (บาท)", 0, value=1590)
    product_cost = c2.number_input("ต้นทุนสินค้า (ไม่รวม Fee/Ads)", 0, value=600)
    
    # --- 3. ADS CALCULATOR (ส่วนที่แก้เพิ่ม) ---
    st.markdown("##### 📢 คำนวณค่าแอด (Ads Cost)")
    
    ads_mode = st.radio("วิธีคิดค่าแอด:", ["ระบุเป็น % ยอดขาย (ง่ายสุด)", "ระบุงบรวม (Budget)", "ระบุเป็นบาท/ชิ้น (ขั้นสูง)"], horizontal=True)
    
    if ads_mode == "ระบุเป็น % ยอดขาย (ง่ายสุด)":
        st.markdown("""<div class="helper-box">💡 <b>แนะนำ:</b> สินค้าทั่วไปควรเผื่อค่าแอด <b>20-30%</b> ของราคาขาย</div>""", unsafe_allow_html=True)
        ads_percent = st.slider("จะเผื่อค่าแอดกี่ % ของยอดขาย?", 0, 50, 25)
        ads_cost = avg_price * (ads_percent / 100)
        st.info(f"👉 คิดเป็นค่าแอด: **{ads_cost:,.0f} บาท/ชิ้น**")
        
    elif ads_mode == "ระบุงบรวม (Budget)":
        st.markdown("""<div class="helper-box">💡 กรอกงบที่มี และจำนวนออเดอร์ที่คาดว่าจะขายได้</div>""", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        total_ad_budget = col_b1.number_input("งบแอดทั้งเดือน (บาท)", 0, value=30000)
        expected_orders = col_b2.number_input("คาดว่าจะขายได้ (ชิ้น)", 0, value=100)
        
        if expected_orders > 0:
            ads_cost = total_ad_budget / expected_orders
            st.info(f"👉 ตกต้นทุนแอด: **{ads_cost:,.0f} บาท/ชิ้น**")
        else:
            ads_cost = 0

    else: # ระบุเป็นบาท (Manual)
        ads_cost = st.number_input("ใส่ค่าแอดต่อชิ้นเอง (บาท)", 0, value=300)

    # 4. FIXED COST
    fixed_cost = st.number_input("ค่าใช้จ่ายคงที่ร้าน (บาท)", 0, value=20000, help="ค่าเช่า, ค่าเน็ต, เงินเดือนตัวเอง")

    # --- CALCULATION ---
    fee_baht = avg_price * (fee_percent / 100)
    total_variable_cost = product_cost + fee_baht + ads_cost
    profit_per_unit = avg_price - total_variable_cost

    st.markdown("---")
    
    if profit_per_unit <= 0:
        st.error(f"❌ **ขาดทุนตั้งแต่ยังไม่เริ่ม!** ติดลบ {profit_per_unit:,.0f} บาท/ชิ้น (ค่าแอดหรือต้นทุนสูงไป)")
    else:
        required_gross_profit = target_profit + fixed_cost
        required_units = math.ceil(required_gross_profit / profit_per_unit)
        daily_units = math.ceil(required_units / 30)
        
        st.markdown(f"""
        <div class="target-box">
            <h3>🔥 ภารกิจวันนี้ (Daily Mission)</h3>
            <div class="daily-mission">{daily_units} ออเดอร์</div>
            <p>กำไรต่อชิ้นของคุณคือ: <b>{profit_per_unit:,.0f} บาท</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 ดูโครงสร้างต้นทุน (คลิก)"):
            st.write(f"1. ราคาขาย: {avg_price} บาท")
            st.write(f"2. หัก ต้นทุนของ: -{product_cost} บาท")
            st.write(f"3. หัก ค่าธรรมเนียม ({fee_percent}%): -{fee_baht:,.0f} บาท")
            st.write(f"4. หัก ค่าแอด (ประมาณการ): -{ads_cost:,.0f} บาท")
            st.write(f"**= เหลือจริง: {profit_per_unit:,.0f} บาท/ชิ้น**")

# ==========================================
# PAGE 2: 🛡️ AUTO PRICE
# ==========================================
elif menu == "🛡️ คิดราคาขาย (Auto Price)":
    st.title("🛡️ เครื่องคิดเลขกันเจ๊ง")
    st.caption("ช่วยตั้งราคาขาย แบบรวมค่าแอดให้แล้ว")

    # 1. PLATFORM
    col_top1, col_top2 = st.columns(2)
    with col_top1:
        platform_shield = st.selectbox("ขายที่ไหน?", list(PLATFORM_FEES.keys()), index=0)
    with col_top2:
        has_vat = st.checkbox("ร้านจด VAT 7%?", value=False)

    # 2. INPUTS
    col_main1, col_main2 = st.columns(2)
    selling_price = col_main1.number_input("ราคาที่จะตั้งขาย (บาท)", 0.0, value=1290.0, step=10.0)
    cost_price = col_main2.number_input("ต้นทุนสินค้า (รวมแพ็ค)", 0.0, value=450.0, step=10.0)
    
    # 3. ADS HELPER (จุดที่แก้เพิ่ม)
    st.markdown("##### 📢 ประมาณการค่าแอด")
    with st.expander("⚙️ ตั้งค่าคำนวณค่าแอด", expanded=True):
        ads_method = st.radio("เลือกวิธีคิด:", ["คิดเป็น % ยอดขาย", "ใส่ยอดเงินเอง"], horizontal=True)
        if ads_method == "คิดเป็น % ยอดขาย":
            ads_pc = st.slider("เผื่อค่าแอดกี่ %", 0, 60, 25)
            ads_per_order = selling_price * (ads_pc / 100)
            st.caption(f"*คิดเป็นเงินประมาณ {ads_per_order:,.0f} บาท*")
        else:
            ads_per_order = st.number_input("ระบุค่าแอดต่อบ้าน (บาท)", 0.0, value=300.0)
            
        auto_fee_rate = PLATFORM_FEES[platform_shield]
        gp_fee = st.number_input(f"ค่าธรรมเนียม {platform_shield} (%)", 0.0, value=auto_fee_rate)

    # --- CALCULATION ---
    if selling_price > 0:
        net_selling_price = selling_price * 100 / 107 if has_vat else selling_price
        vat_amt = selling_price - net_selling_price
        fee_amt = selling_price * (gp_fee / 100)
        
        total_deduct = cost_price + fee_amt + ads_per_order + vat_amt
        net_profit = selling_price - total_deduct
        margin_percent = (net_profit / selling_price) * 100

        st.markdown("---")
        if net_profit > 0:
            st.markdown(f"""
            <div style="text-align:center;">
                <h1 style="color:#28a745;">+{net_profit:,.0f} บาท</h1>
                <p>กำไรเข้ากระเป๋า <b>{margin_percent:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            if margin_percent < 20: st.warning("⚠️ กำไรน้อยกว่า 20% (เสี่ยงไม่คุ้มเหนื่อย)")
        else:
            st.error(f"❌ ขาดทุน {net_profit:,.0f} บาท (ค่าแอด/ต้นทุนสูงเกินไป)")

# ==========================================
# PAGE 3 & 4 (เหมือนเดิม)
# ==========================================
elif menu == "📢 ตรวจค่าแอด (Ads Doctor)":
    # (Copy Code เดิมส่วน Ads Doctor มาใส่ หรือใช้ Code ย่อด้านล่าง)
    st.title("📢 หมอตรวจแอด")
    ad_spend = st.number_input("งบที่ใช้ (Ad Spend)", 0.0, value=5000.0)
    sales = st.number_input("ยอดขายที่ได้ (GMV)", 0.0, value=15000.0)
    margin = st.slider("กำไรขั้นต้นสินค้า (%)", 10, 90, 40)
    if ad_spend > 0:
        roas = sales/ad_spend
        be_roas = 100/margin
        st.metric("ROAS จริง vs ขั้นต่ำ", f"{roas:.2f} vs {be_roas:.2f}")
        if roas >= be_roas: st.success("✅ กำไร")
        else: st.error("❌ ขาดทุน")

elif menu == "🏥 ตรวจสุขภาพร้าน (Cash Flow)":
    # (Copy Code เดิมส่วน Cash Flow มาใส่)
    st.title("🏥 ตรวจสุขภาพการเงิน")
    cash = st.number_input("เงินสด", 0, value=50000)
    debt = st.number_input("หนี้สิน", 0, value=30000)
    expense = st.number_input("รายจ่ายคงที่", 0, value=20000)
    runway = (cash-debt)/expense if expense>0 else 99
    st.metric("อยู่ได้อีก (เดือน)", f"{runway:.1f}")
