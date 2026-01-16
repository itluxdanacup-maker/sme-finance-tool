import streamlit as st
import math

# --- 1. SETTING ---
st.set_page_config(page_title="Merchant Commander V6", page_icon="👑", layout="centered")

st.markdown("""
<style>
    .mission-box { background-color: #e3f2fd; padding: 20px; border-radius: 15px; border: 2px solid #2196f3; text-align: center; margin-bottom: 20px;}
    .big-number { font-size: 48px !important; font-weight: bold; color: #0d47a1; }
    .ad-budget-box { background-color: #fff3cd; padding: 15px; border-radius: 10px; border: 1px dashed #ffc107; text-align: center; margin-top: 10px;}
    .money-text { color: #28a745; font-weight: bold; font-size: 24px; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=80)
    st.title("ระบบบัญชาการร้าน")
    menu = st.radio("เลือกเมนู:", ["🎯 ตั้งเป้าหมาย (Mission)", "🛡️ คำนวณกำไร (Margin)"])
    st.caption("V6: สำหรับร้านสินค้าเยอะ")

# ==========================================
# PAGE 1: 🎯 MISSION CONTROL (แบบใหม่)
# ==========================================
if menu == "🎯 ตั้งเป้าหมาย (Mission)":
    st.title("🎯 Mission Commander")
    st.caption("คำนวณเป้าหมายรายวัน + งบแอดที่ต้องใช้")

    # 1. GOAL & COST
    st.subheader("1. เป้าหมาย & รายจ่ายคงที่")
    col1, col2 = st.columns(2)
    target_profit = col1.number_input("อยากได้กำไรสุทธิเดือนนี้ (บาท)", 0, value=100000, step=5000, help="เงินเหลือเก็บเข้ากระเป๋าจริงๆ")
    fixed_cost = col2.number_input("ค่าใช้จ่ายคงที่ร้าน (บาท)", 0, value=20000, help="ค่าเช่า, เงินเดือนแอดมิน, ค่าเน็ต")

    st.markdown("---")
    
    # 2. MARGIN & ADS (หัวใจสำคัญ)
    st.subheader("2. โครงสร้างกำไร (กะประมาณเป็น %)")
    st.info("💡 ร้านสินค้าเยอะ ไม่ต้องใส่ราคาต่อชิ้น ให้ใส่เป็น % ภาพรวมแทน")
    
    col3, col4 = st.columns(2)
    # Gross Profit Margin
    gross_margin_pct = col3.slider("กำไรขั้นต้นโดยเฉลี่ย (%)", 10, 90, 40, help="เช่น ขาย 100 บาท ต้นทุนของ 60 บาท = กำไร 40%")
    # Ads Cost %
    ads_pct = col4.slider("งบยิงแอดต่อยอดขาย (%)", 5, 50, 20, help="ขาย 100 บาท ยอมจ่ายค่าแอดกี่บาท?")
    
    # Platform Fee
    platform_fee = st.number_input("ค่าธรรมเนียม Platform (%)", 0.0, value=12.0, help="Shopee ~12%, TikTok ~8%")
    
    # Basket Size (เพื่อหาจำนวนออเดอร์)
    avg_basket_size = st.number_input("ยอดขายต่อบิลโดยประมาณ (บาท)", 0, value=500, help="ปกติลูกค้าซื้อครั้งละกี่บาท (เอาไว้คำนวณจำนวนออเดอร์)")

    # --- CALCULATION LOGIC ---
    # 1. Net Margin % (กำไรสุทธิที่เหลือเป็นเปอร์เซ็นต์)
    # สูตร: กำไรขั้นต้น - ค่าแอด - ค่าธรรมเนียม
    net_margin_pct = gross_margin_pct - ads_pct - platform_fee
    
    st.markdown("---")

    if net_margin_pct <= 0:
        st.error(f"❌ **เป็นไปไม่ได้!** โครงสร้างราคานี้คุณขาดทุน {net_margin_pct:.1f}%")
        st.warning("คำแนะนำ: ต้องเพิ่มกำไรขั้นต้น หรือ ลดงบแอดลง")
    else:
        # 2. Required Sales (ยอดขายที่ต้องทำได้ เพื่อให้ครอบคลุม Target + Fixed Cost)
        total_required_money = target_profit + fixed_cost
        required_sales = total_required_money / (net_margin_pct / 100)
        
        # 3. Breakdown Daily
        daily_sales = required_sales / 30
        daily_orders = math.ceil(daily_sales / avg_basket_size) if avg_basket_size > 0 else 0
        
        # 4. ADS BUDGET CALCULATION (ตามที่ขอมา)
        # งบแอดวันนี้ = ยอดขายเป้าหมายวันนี้ x %ค่าแอด
        daily_ads_budget = daily_sales * (ads_pct / 100)

        # --- OUTPUT DISPLAY ---
        st.markdown(f"""
        <div class="mission-box">
            <h3>🔥 ภารกิจวันนี้ (Daily Mission)</h3>
            <div class="big-number">{daily_orders} ออเดอร์</div>
            <p>ยอดขายเป้าหมาย: <b>{daily_sales:,.0f} บาท/วัน</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ad-budget-box">
            <h4>📢 งบแอดที่ต้องเติมวันนี้</h4>
            <div class="money-text">{daily_ads_budget:,.0f} บาท</div>
            <small>(คิดจาก {ads_pct}% ของยอดขายเป้าหมาย)</small>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 ดูรายละเอียดการคำนวณ"):
            st.write(f"**1. เปอร์เซ็นต์กำไรเหลือจริง:** {net_margin_pct:.1f}%")
            st.write(f"*(มาจาก: กำไรสินค้า {gross_margin_pct}% - แอด {ads_pct}% - Fee {platform_fee}%)*")
            st.write(f"**2. ต้องหาเงินทั้งหมด:** {total_required_money:,.0f} บาท (กำไร+ค่าเช่า)")
            st.write(f"**3. ต้องมียอดขายรวม:** {required_sales:,.0f} บาท")
            st.write(f"**4. ยอดขายต่อวัน:** {daily_sales:,.0f} บาท")

# ==========================================
# PAGE 2: 🛡️ MARGIN CHECKER (เช็ครายตัว)
# ==========================================
elif menu == "🛡️ คำนวณกำไร (Margin)":
    st.title("🛡️ เช็คกำไรรายสินค้า")
    st.caption("สำหรับลองคำนวณสินค้าเฉพาะตัว ว่าคุ้มไหม")
    
    price = st.number_input("ราคาขาย", 0.0, value=500.0)
    cost = st.number_input("ต้นทุนของ", 0.0, value=250.0)
    fee = st.number_input("ค่าธรรมเนียม (%)", 0.0, value=12.0)
    ads = st.number_input("งบแอด (%)", 0.0, value=20.0)
    
    if price > 0:
        fee_baht = price * (fee/100)
        ads_baht = price * (ads/100)
        profit = price - cost - fee_baht - ads_baht
        
        st.markdown("---")
        if profit > 0:
            st.success(f"✅ กำไร {profit:,.0f} บาท ({profit/price*100:.1f}%)")
        else:
            st.error(f"❌ ขาดทุน {profit:,.0f} บาท")
