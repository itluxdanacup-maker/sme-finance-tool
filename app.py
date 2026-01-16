import streamlit as st
import pandas as pd
import math

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Seller Super App Auto", page_icon="🛍️", layout="centered")

st.markdown("""
<style>
    .big-stat { font-size: 28px !important; font-weight: bold; color: #333; text-align: center; }
    .target-box { background-color: #e0f7fa; padding: 20px; border-radius: 15px; border: 2px solid #00bcd4; text-align: center; margin-bottom: 20px;}
    .daily-mission { font-size: 42px !important; font-weight: bold; color: #0097a7; }
    .auto-tag { background-color: #d1ecf1; color: #0c5460; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURATION (ฐานข้อมูลค่าธรรมเนียมกลาง) ---
# แก้ไขค่า Default ตรงนี้ได้เลย
PLATFORM_FEES = {
    "Website / Facebook (โอนเอง)": 0.0,
    "TikTok Shop": 8.0,       # ประมาณ 8% (รวม VAT)
    "Shopee (Non-Mall)": 12.0, # ประมาณ 12% (ค่าคอม+ธุรกรรม+ส่งฟรี+VAT)
    "Lazada (General)": 12.0,  # ใกล้เคียง Shopee
    "LINE SHOPPING": 3.0       # ประมาณ 3%
}

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=80)
    st.title("ระบบจัดการร้าน")
    menu = st.radio("เลือกเมนู:", 
        ["🎯 ตั้งเป้าหมาย (Mission)",
         "🛡️ คิดราคาขาย (Auto Price)", 
         "📢 ตรวจค่าแอด (Ads Doctor)", 
         "🏥 ตรวจสุขภาพร้าน (Cash Flow)"])
    st.caption("V4.0 (Auto-Pilot Mode)")

# ==========================================
# PAGE 1: 🎯 MISSION CONTROL (AUTO)
# ==========================================
if menu == "🎯 ตั้งเป้าหมาย (Mission)":
    st.title("🎯 Mission Commander")
    st.caption("แค่บอกว่าอยากรวยเท่าไหร่ ที่เหลือระบบคำนวณให้")

    # 1. INPUT ความฝัน
    target_profit = st.number_input("เดือนนี้อยากได้กำไรเข้ากระเป๋า (บาท)", 0, value=100000, step=5000)
    
    st.markdown("---")
    st.markdown("##### 🛒 ข้อมูลสินค้า (ค่าเฉลี่ย)")
    
    # 2. PLATFORM SELECTOR (พระเอกของงานนี้)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        selected_platform = st.selectbox("ส่วนใหญ่ขายที่ไหน?", list(PLATFORM_FEES.keys()), index=2) # Default Shopee
    with col_p2:
        # Auto-fill ค่าธรรมเนียมตามที่เลือก
        default_fee = PLATFORM_FEES[selected_platform]
        fee_percent = st.number_input(f"ค่าธรรมเนียม {selected_platform} (%)", 0.0, value=default_fee, step=0.5, help="ระบบใส่ค่ามาตรฐานให้ แต่แก้เองได้")

    # 3. COST INPUTS
    c1, c2 = st.columns(2)
    avg_price = c1.number_input("ราคาขายเฉลี่ย (บาท)", 0, value=1590)
    product_cost = c2.number_input("ต้นทุนสินค้าจริง (ไม่รวม Fee)", 0, value=600, help="ค่าของ + ค่าแพ็ค (ไม่ต้องบวกค่าธรรมเนียม เดี๋ยวระบบคิดให้)")
    
    c3, c4 = st.columns(2)
    fixed_cost = c3.number_input("ค่าใช้จ่ายคงที่ร้าน (บาท)", 0, value=20000)
    ads_cost = c4.number_input("ค่าแอดเฉลี่ยต่อออเดอร์ (บาท)", 0, value=250)

    # --- AUTO CALCULATION ---
    # คำนวณค่าธรรมเนียมเป็นบาทอัตโนมัติ
    fee_baht = avg_price * (fee_percent / 100)
    total_variable_cost = product_cost + fee_baht + ads_cost
    profit_per_unit = avg_price - total_variable_cost

    st.markdown("---")
    
    if profit_per_unit <= 0:
        st.error(f"❌ **ขายขาดทุน!** หักลบแล้วติดลบ {profit_per_unit:,.0f} บาทต่อชิ้น (ยังไม่ทันจ่ายค่าเช่าร้านเลย)")
        st.warning(f"แนะนำ: ต้องขึ้นราคา หรือลดต้นทุนแอด/ค่าของ ด่วน!")
    else:
        # คำนวณเป้าหมาย
        required_gross_profit = target_profit + fixed_cost
        required_units = math.ceil(required_gross_profit / profit_per_unit)
        daily_units = math.ceil(required_units / 30)
        
        # แสดงผลแบบการ์ดสวยๆ
        st.markdown(f"""
        <div class="target-box">
            <h3>🔥 ภารกิจวันนี้ (Daily Mission)</h3>
            <div class="daily-mission">{daily_units} ออเดอร์</div>
            <p>กำไรต่อชิ้นของคุณคือ: <b>{profit_per_unit:,.0f} บาท</b> (หักทุกอย่างแล้ว)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown ย่อย
        with st.expander("🔍 ดูที่มาของตัวเลข (ระบบคิดให้แบบนี้)"):
            st.write(f"1. ราคาขาย: {avg_price} บาท")
            st.write(f"2. หัก ต้นทุนของ: -{product_cost} บาท")
            st.write(f"3. หัก ค่าธรรมเนียม ({fee_percent}%): -{fee_baht:,.0f} บาท (Auto)")
            st.write(f"4. หัก ค่าแอด: -{ads_cost} บาท")
            st.write(f"**= เหลือจริงต่อชิ้น: {profit_per_unit:,.0f} บาท**")
            st.write(f"--------------------------------")
            st.write(f"ต้องหาเงินจ่าย Fix Cost: {fixed_cost:,} บาท")
            st.write(f"อยากได้กำไรส่วนตัว: {target_profit:,} บาท")
            st.write(f"รวมต้องหาเงิน: {required_gross_profit:,} บาท -> หารกำไรต่อชิ้น -> ได้เป้าหมาย!")

# ==========================================
# PAGE 2: 🛡️ AUTO PRICE (PROFIT SHIELD)
# ==========================================
elif menu == "🛡️ คิดราคาขาย (Auto Price)":
    st.title("🛡️ เครื่องคิดเลขกันเจ๊ง (Auto)")
    st.caption("เลือกแพลตฟอร์ม -> ใส่ทุน -> รู้เรื่อง!")

    # 1. PLATFORM & VAT (บนสุด)
    col_top1, col_top2 = st.columns(2)
    with col_top1:
        platform_shield = st.selectbox("จะขายที่ไหน?", list(PLATFORM_FEES.keys()), index=2)
    with col_top2:
        has_vat = st.checkbox("ร้านจด VAT 7% ไหม?", value=True)

    # 2. MAIN INPUTS
    col_main1, col_main2 = st.columns(2)
    selling_price = col_main1.number_input("ราคาที่จะตั้งขาย (บาท)", 0.0, value=1590.0, step=10.0)
    cost_price = col_main2.number_input("ต้นทุนสินค้า (รวมแพ็ค)", 0.0, value=600.0, step=10.0)
    
    # 3. HIDDEN FEES (Auto-filled but editable)
    with st.expander("⚙️ ตั้งค่าธรรมเนียม & ค่าแอด (แก้ไขได้)", expanded=True):
        c3, c4 = st.columns(2)
        # ดึงค่า Default มาใส่ให้เลย
        auto_fee = PLATFORM_FEES[platform_shield]
        gp_fee = c3.number_input(f"Fee {platform_shield} (%)", 0.0, value=auto_fee)
        ads_per_order = c4.number_input("ค่าแอดต่อบ้าน (บาท)", 0.0, value=250.0)

    # --- CALCULATION ---
    if selling_price > 0:
        # Logic ภาษี & Fee
        net_selling_price = selling_price * 100 / 107 if has_vat else selling_price
        vat_amt = selling_price - net_selling_price
        fee_amt = selling_price * (gp_fee / 100)
        
        total_deduct = cost_price + fee_amt + ads_per_order + vat_amt
        net_profit = selling_price - total_deduct
        margin_percent = (net_profit / selling_price) * 100

        st.markdown("---")
        # แสดงผลตัวใหญ่ๆ
        if net_profit > 0:
            st.markdown(f"""
            <div style="text-align:center;">
                <h1 style="color:#28a745; margin-bottom:0;">+{net_profit:,.0f} บาท</h1>
                <p style="font-size:18px;">กำไรสุทธิ <b>{margin_percent:.1f}%</b> (เข้ากระเป๋าจริง)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Bar Chart ง่ายๆ
            st.progress(min(margin_percent/100, 1.0))
            if margin_percent < 15:
                st.warning("⚠️ กำไรบางมาก (ต่ำกว่า 15%) เหนื่อยฟรีระวังไม่คุ้ม")
            else:
                st.success("✅ กำไรสวย! ลุยได้เลย")
                
        else:
            st.markdown(f"""
            <div style="text-align:center;">
                <h1 style="color:#dc3545; margin-bottom:0;">{net_profit:,.0f} บาท</h1>
                <p style="font-size:18px;">❌ ขาดทุนยับ!</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PAGE 3 & 4 (เหมือนเดิม)
# ==========================================
elif menu == "📢 ตรวจค่าแอด (Ads Doctor)":
    st.title("📢 หมอตรวจแอด")
    # (Copy Logic เดิมมาใส่ได้เลย หรือใช้ตัวย่อนี้)
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
    st.title("🏥 ตรวจสุขภาพการเงิน")
    # (Logic เดิม)
    cash = st.number_input("เงินสด", 0, value=50000)
    debt = st.number_input("หนี้สิน", 0, value=30000)
    expense = st.number_input("รายจ่ายคงที่", 0, value=20000)
    runway = (cash-debt)/expense if expense>0 else 99
    st.metric("อยู่ได้อีก (เดือน)", f"{runway:.1f}")
    if runway < 3: st.warning("สภาพคล่องต่ำ")
