import streamlit as st
import pandas as pd
import math

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Seller Super App Pro", page_icon="🚀", layout="centered")

st.markdown("""
<style>
    /* Styling */
    .big-stat { font-size: 28px !important; font-weight: bold; color: #333; text-align: center; }
    .target-box { background-color: #e3f2fd; padding: 20px; border-radius: 15px; border: 2px solid #2196f3; text-align: center; margin-bottom: 20px;}
    .daily-mission { font-size: 40px !important; font-weight: bold; color: #d63384; }
    .card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #ddd; }
    section[data-testid="stSidebar"] { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=80)
    st.title("Seller Command Center")
    menu = st.radio("เลือกปฏิบัติการ:", 
        ["🎯 ตั้งเป้าหมาย (Mission Control)",
         "🛡️ คิดราคาขาย (Profit)", 
         "📢 ตรวจค่าแอด (Ads Doctor)", 
         "🏥 ตรวจสุขภาพร้าน (Cash Flow)"])
    
    st.markdown("---")
    st.caption("Version 3.0 (Mission Commander)")

# ==========================================
# PAGE 1: 🎯 MISSION CONTROL (NEW FEATURE)
# ==========================================
if menu == "🎯 ตั้งเป้าหมาย (Mission Control)":
    st.title("🎯 Mission Commander")
    st.caption("เปลี่ยนฝันให้เป็นเป้าหมายรายวัน")

    # 1. INPUT เป้าหมาย
    st.markdown("##### 1. ความฝันของคุณ")
    target_profit = st.number_input("เดือนนี้อยากได้กำไรสุทธิกี่บาท? (เข้ากระเป๋า)", 0, value=100000, step=5000)
    
    st.markdown("##### 2. ข้อมูลสินค้า (ค่าเฉลี่ย)")
    c1, c2 = st.columns(2)
    avg_price = c1.number_input("ราคาขายเฉลี่ยต่อชิ้น", 0, value=1590)
    avg_cost = c2.number_input("ต้นทุนสินค้า + ค่าธรรมเนียม", 0, value=900, help="ต้นทุนของ + ค่ากล่อง + ค่า GP Lazada/Shopee")
    
    st.markdown("##### 3. ค่าใช้จ่ายดำเนินงาน")
    c3, c4 = st.columns(2)
    fixed_cost = c3.number_input("ค่าใช้จ่ายคงที่ (เงินเดือน/เช่า)", 0, value=20000)
    ads_cost_per_sale = c4.number_input("ค่าแอดเฉลี่ยต่อออเดอร์ (CPR)", 0, value=250)

    # Calculation Logic
    # สูตร: (Unit_Price - Unit_Cost - Ads) * Units - Fixed_Cost = Target_Profit
    # ย้ายข้างหา Units: Units = (Target_Profit + Fixed_Cost) / (Unit_Price - Unit_Cost - Ads)
    
    profit_per_unit = avg_price - avg_cost - ads_cost_per_sale
    
    st.markdown("---")
    
    if profit_per_unit <= 0:
        st.error(f"❌ เป็นไปไม่ได้! สินค้าคุณขาดทุนต่อชิ้น {profit_per_unit:,.0f} บาท (ยังไม่ทันหัก Fix Cost เลย)")
    else:
        # คำนวณเป้าหมาย
        required_gross_profit = target_profit + fixed_cost
        required_units = math.ceil(required_gross_profit / profit_per_unit)
        required_sales_vol = required_units * avg_price
        estimated_ads_budget = required_units * ads_cost_per_sale
        
        # Daily Target (คิด 30 วัน)
        daily_units = math.ceil(required_units / 30)
        daily_sales = required_sales_vol / 30

        # --- OUTPUT: MISSION CARD ---
        st.markdown(f"""
        <div class="target-box">
            <h3>🔥 ภารกิจประจำวันของคุณ (Daily Mission)</h3>
            <div class="daily-mission">{daily_units} ออเดอร์ / วัน</div>
            <p>หรือยอดขาย {daily_sales:,.0f} บาท/วัน</p>
        </div>
        """, unsafe_allow_html=True)

        # Detail Stats
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("📦 เป้าทั้งเดือน (ชิ้น)", f"{required_units:,}")
        c_res2.metric("💰 ยอดขายรวม (GMV)", f"{required_sales_vol:,.0f}")
        c_res3.metric("📢 เตรียมงบแอด", f"{estimated_ads_budget:,.0f}")
        
        st.info(f"💡 **Tip:** คุณต้องทำกำไรต่อชิ้นให้ได้ **{profit_per_unit:,.0f} บาท** เพื่อครอบคลุมค่าใช้จ่ายคงที่และกำไรที่ตั้งเป้าไว้")

# ==========================================
# PAGE 2: 🛡️ PROFIT SHIELD
# ==========================================
elif menu == "🛡️ คิดราคาขาย (Profit)":
    st.title("🛡️ เครื่องคิดเลขกันเจ๊ง")
    # ... (Code เดิมจาก Profit Calculator) ...
    with st.container():
        c1, c2 = st.columns(2)
        selling_price = c1.number_input("ราคาขาย (บาท)", 0.0, value=1590.0, step=10.0)
        cost_price = c2.number_input("ต้นทุนของ (รวมแพ็ค)", 0.0, value=650.0, step=10.0)
        c3, c4 = st.columns(2)
        gp_fee = c3.number_input("ค่าธรรมเนียม Platform (%)", 0.0, value=12.0)
        ads_per_order = c4.number_input("ค่าแอดต่อบ้าน (บาท)", 0.0, value=250.0)
        has_vat = st.checkbox("จด VAT 7%", value=True)

    if selling_price > 0:
        net_selling_price = selling_price * 100 / 107 if has_vat else selling_price
        vat_amt = selling_price - net_selling_price
        fee_amt = selling_price * (gp_fee / 100)
        total_deduct = cost_price + fee_amt + ads_per_order + vat_amt
        net_profit = selling_price - total_deduct
        margin_percent = (net_profit / selling_price) * 100

        st.markdown("---")
        if net_profit > 0:
            st.markdown(f"<div class='big-stat' style='color:#28a745'>+{net_profit:,.0f} บาท ({margin_percent:.1f}%)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='big-stat' style='color:#dc3545'>{net_profit:,.0f} บาท</div>", unsafe_allow_html=True)
            st.error("ขาดทุน!")

# ==========================================
# PAGE 3: 📢 ADS DOCTOR
# ==========================================
elif menu == "📢 ตรวจค่าแอด (Ads Doctor)":
    st.title("📢 หมอตรวจแอด")
    # ... (Code เดิมจาก Ads Doctor) ...
    col_a1, col_a2 = st.columns(2)
    ad_spend = col_a1.number_input("งบที่ใช้ไป", 0.0, value=5000.0)
    sales_from_ads = col_a2.number_input("ยอดขายที่ได้", 0.0, value=15000.0)
    profit_margin_percent = st.slider("กำไรขั้นต้นสินค้า (%)", 10, 90, 40)
    st.markdown("---")
    
    if ad_spend > 0 and sales_from_ads > 0:
        actual_roas = sales_from_ads / ad_spend
        breakeven_roas = 1 / (profit_margin_percent / 100)
        net_ads_profit = (sales_from_ads * (profit_margin_percent / 100)) - ad_spend
        
        c1, c2 = st.columns(2)
        c1.metric("ROAS จริง", f"{actual_roas:.2f}")
        c2.metric("ROAS ขั้นต่ำที่รอด", f"{breakeven_roas:.2f}")
        
        if actual_roas >= breakeven_roas:
            st.success(f"✅ กำไร {net_ads_profit:,.0f} บาท")
        else:
            st.error(f"❌ ขาดทุน {abs(net_ads_profit):,.0f} บาท")

# ==========================================
# PAGE 4: 🏥 HEALTH CHECK
# ==========================================
elif menu == "🏥 ตรวจสุขภาพร้าน (Cash Flow)":
    st.title("🏥 ตรวจสุขภาพการเงิน")
    # ... (Code เดิมจาก Cash Flow) ...
    c1, c2, c3 = st.columns(3)
    cash = c1.number_input("เงินสด", 0, value=50000)
    debt = c2.number_input("หนี้ (30วัน)", 0, value=30000)
    expense = c3.number_input("รายจ่ายคงที่", 0, value=20000)
    
    liquidity = cash - debt
    runway = (cash - debt) / expense if expense > 0 else 99
    
    st.metric("สภาพคล่องสุทธิ", f"{liquidity:,.0f}")
    st.metric("อยู่ได้อีก (เดือน)", f"{runway:.1f}")
    if runway < 3: st.warning("ระวัง! สภาพคล่องต่ำ")
