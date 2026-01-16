import streamlit as st
import pandas as pd
import math

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Money Master V7", page_icon="💸", layout="centered")

st.markdown("""
<style>
    .money-mission-box { 
        background-color: #e8f5e9; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #4caf50; 
        text-align: center; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .big-money-target { font-size: 52px !important; font-weight: 800; color: #2e7d32; line-height: 1.2;}
    .sub-text { font-size: 18px; color: #555; }
    
    .ads-box { 
        background-color: #fff3cd; 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px dashed #ffc107; 
        text-align: center;
        margin-top: 20px;
    }
    .ads-amount { font-size: 36px !important; font-weight: bold; color: #d39e00; }
    
    section[data-testid="stSidebar"] { background-color: #fafafa; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2454/2454282.png", width=80)
    st.title("ระบบบัญชาการเงิน")
    menu = st.radio("เมนู:", ["🎯 เป้าหมายวันนี้ (Mission)", "🛡️ เช็คกำไรรายตัว"])
    st.caption("V7: Money Master Mode")

# ==========================================
# PAGE 1: 🎯 MISSION CONTROL (NO BASKET SIZE)
# ==========================================
if menu == "🎯 เป้าหมายวันนี้ (Mission)":
    st.title("🎯 Mission Commander")
    st.caption("เน้นยอดขายรวม ไม่ต้องสนออเดอร์เฉลี่ย")

    # 1. INPUT (เป้าหมาย & รายจ่าย)
    st.subheader("1. อยากเหลือเงินเท่าไหร่?")
    col1, col2 = st.columns(2)
    target_profit = col1.number_input("กำไรเข้ากระเป๋า (บาท/เดือน)", 0, value=100000, step=5000)
    fixed_cost = col2.number_input("ค่าใช้จ่ายร้าน (บาท/เดือน)", 0, value=25000, help="ค่าเช่า, ค่าพนักงาน, ค่าระบบ")

    st.markdown("---")
    
    # 2. PROFIT STRUCTURE (กะเป็น % ภาพรวม)
    st.subheader("2. โครงสร้างราคาร้านเรา (กะประมาณ)")
    
    c1, c2 = st.columns(2)
    gross_margin_pct = c1.slider("กำไรขั้นต้นสินค้าโดยเฉลี่ย (%)", 10, 90, 40, help="ขาย 100 บาท ทุนของกี่บาท? (ถ้าทุน 60 คือกำไร 40%)")
    platform_fee = c2.number_input("ค่าธรรมเนียม Platform (%)", 0.0, value=12.0)
    
    st.info("📢 **เรื่องค่าแอด:** ไม่ต้องกรอก ระบบจะแนะนำให้ตามมาตรฐานธุรกิจ (20-25%) หรือคุณจะกำหนดเองก็ได้")
    use_manual_ads = st.checkbox("กำหนด % ค่าแอดเอง (ปกติระบบคิดให้ที่ 20%)")
    
    if use_manual_ads:
        ads_pct = st.slider("ยอมจ่ายค่าแอดกี่ % ของยอดขาย", 5, 50, 25)
    else:
        ads_pct = 20.0 # ค่ามาตรฐาน
    
    # --- CALCULATION CORE ---
    # 1. Net Margin ที่เหลือจริง (หลังหัก แอด + Fee)
    net_margin_pct = gross_margin_pct - platform_fee - ads_pct
    
    st.markdown("---")

    if net_margin_pct <= 0:
        st.error(f"❌ **โครงสร้างนี้เจ๊งครับ!** หักค่าแอดกับค่าธรรมเนียมแล้ว ติดลบ {net_margin_pct:.1f}%")
        st.warning("ทางแก้: ต้องลดงบแอดลง หรือ หาร้านค้าที่ค่าธรรมเนียมถูกลง หรือ ขึ้นราคาสินค้า")
    else:
        # 2. คำนวณยอดเงินที่ต้องหา (Reverse Calc)
        total_needed = target_profit + fixed_cost
        required_monthly_sales = total_needed / (net_margin_pct / 100)
        daily_sales_target = required_monthly_sales / 30
        
        # 3. คำนวณงบแอดรายวัน
        daily_ads_budget = daily_sales_target * (ads_pct / 100)

        # --- OUTPUT: BIG NUMBERS ---
        st.markdown(f"""
        <div class="money-mission-box">
            <div class="sub-text">🔥 ภารกิจยอดขายวันนี้ (Daily Sales)</div>
            <div class="big-money-target">{daily_sales_target:,.0f} บาท</div>
            <div class="sub-text">ต้องทำให้ได้ยอดนี้ ถึงจะเข้าเป้าสิ้นเดือน</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="ads-box">
            <div class="sub-text">📢 งบยิงแอดแนะนำวันนี้ (Ads Budget)</div>
            <div class="ads-amount">{daily_ads_budget:,.0f} บาท</div>
            <div class="sub-text">คิดเป็น {ads_pct}% ของเป้ายอดขาย (ยิงเกินนี้กำไรหด)</div>
        </div>
        """, unsafe_allow_html=True)

        # --- SCENARIO TABLE (ตารางความเป็นไปได้) ---
        st.write("### 📦 แล้วต้องแพ็คกี่กล่อง? (ประเมินตามราคาสินค้า)")
        st.caption("เนื่องจากเราไม่รู้ออเดอร์เฉลี่ย นี่คือตารางเทียบให้ดูว่า ถ้าขายของราคาต่างๆ ต้องได้กี่บ้าน")
        
        # สร้างตารางจำลอง
        price_points = [300, 500, 990, 1500, 2500] # ช่วงราคาสินค้าทั่วไป
        scenario_data = []
        
        for p in price_points:
            orders_needed = math.ceil(daily_sales_target / p)
            scenario_data.append({
                "ถ้าขายสินค้าชิ้นละ (บาท)": f"{p:,}",
                "ต้องหาลูกค้า (คน)": f"{orders_needed:,} บ้าน",
                "ค่าแอดต่อบ้าน (CPR)": f"{daily_ads_budget/orders_needed:,.0f} บาท"
            })
            
        df_scenario = pd.DataFrame(scenario_data)
        st.table(df_scenario)
        st.caption("*CPR = Cost Per Result (ค่าแอดเฉลี่ยต่อการขาย 1 ออเดอร์ที่ยอมรับได้)")

# ==========================================
# PAGE 2: 🛡️ MARGIN CHECKER
# ==========================================
elif menu == "🛡️ เช็คกำไรรายตัว":
    st.title("🛡️ เครื่องคิดเลขกำไร (รายชิ้น)")
    st.caption("หยิบสินค้ามาเช็คสักตัว ว่าขายราคานี้คุ้มไหม")
    
    c1, c2 = st.columns(2)
    price = c1.number_input("ราคาขาย (บาท)", 0.0, value=590.0)
    cost = c2.number_input("ต้นทุนของ (บาท)", 0.0, value=250.0)
    
    fee = st.number_input("ค่าธรรมเนียม Platform (%)", 0.0, value=12.0)
    ads = st.number_input("งบแอดที่วางไว้ (%)", 0.0, value=25.0)
    
    if price > 0:
        fee_baht = price * (fee/100)
        ads_baht = price * (ads/100)
        total_cost = cost + fee_baht + ads_baht
        profit = price - total_cost
        margin = (profit / price) * 100
        
        st.markdown("---")
        if profit > 0:
            st.success(f"✅ ขายได้! กำไร {profit:,.0f} บาท ({margin:.1f}%)")
            st.write(f"- หักค่าแอดไป: {ads_baht:,.0f} บาท")
            st.write(f"- หักค่าธรรมเนียม: {fee_baht:,.0f} บาท")
        else:
            st.error(f"❌ ขาดทุน {profit:,.0f} บาท")
