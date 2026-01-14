import streamlit as st
import pandas as pd

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="เครื่องคิดเลขกันเจ๊ง", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    .big-money { font-size: 40px !important; font-weight: bold; color: #28a745; text-align: center;}
    .big-loss { font-size: 40px !important; font-weight: bold; color: #dc3545; text-align: center;}
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
    .stNumberInput input { text-align: right; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🛡️ เครื่องคิดเลขกันเจ๊ง (Super Profit)")
st.caption("หน้าบ้านง่ายๆ แต่หลังบ้านคำนวณเป๊ะ! รวมค่าธรรมเนียมแฝงให้ครบ")

# --- 3. INPUT (กรอกง่ายๆ) ---
with st.container():
    st.subheader("1. ตั้งราคาขาย & ต้นทุน")
    col1, col2 = st.columns(2)
    selling_price = col1.number_input("ราคาขายหน้าร้าน (บาท)", 0.0, value=1700.0, step=10.0)
    cost_price = col2.number_input("ต้นทุนสินค้า (รวมแพ็ค)", 0.0, value=800.0, step=10.0)

    st.subheader("2. ค่าธรรมเนียม & การตลาด (ตัวดูดเงิน)")
    col3, col4 = st.columns(2)
    
    # Platform Fee Logic (ซับซ้อนหลังบ้าน)
    platform = col3.selectbox("ขายที่ไหน?", ["Website/Facebook (โอนเอง)", "Shopee (Non-Mall)", "Lazada (General)", "TikTok Shop"])
    
    # ค่าธรรมเนียมโดยประมาณ (ปรับแก้ได้)
    fee_rates = {
        "Website/Facebook (โอนเอง)": 0.0,
        "Shopee (Non-Mall)": 12.0, # สมมติรวม Com+Trans+VAT
        "Lazada (General)": 12.0,
        "TikTok Shop": 8.0
    }
    
    platform_fee_percent = col3.number_input(f"ค่าธรรมเนียม {platform} (%)", 0.0, value=fee_rates[platform])
    ads_budget = col4.number_input("งบยิงแอด (เฉลี่ยต่อออเดอร์)", 0.0, value=300.0, help="เช่น ยิงแอด 1,000 บาท ขายได้ 10 บ้าน = ตกบ้านละ 100")

    shipping_cost = st.number_input("ค่าส่งที่ร้านช่วยออก (Free Shipping)", 0.0, value=0.0, help="ถ้าลูกค้าจ่ายค่าส่งเอง ใส่ 0")
    
    has_vat = st.checkbox("ร้านจดทะเบียน VAT (7%) หรือไม่?", value=True)

# --- 4. THE BRAIN (หลังบ้านทำงานหนัก) ---
# Logic การคำนวณที่แม่นยำ (Hidden Complexity)

# 1. VAT ขาย (Output VAT)
if has_vat:
    # ถ้าราคาขายรวม VAT แล้ว ต้องถอด VAT ออกมา
    price_before_vat = selling_price * 100 / 107
    vat_amount = selling_price - price_before_vat
else:
    vat_amount = 0

# 2. Platform Fee (คิดจากยอดขายเต็ม)
# ส่วนใหญ่ Platform จะคิด VAT 7% บนค่าธรรมเนียมอีกที (Fee + VAT on Fee)
fee_amount = selling_price * (platform_fee_percent / 100)
# *หมายเหตุ: สูตรนี้คิดแบบรวบยอดเพื่อความง่ายในหน้าบ้าน

# 3. ต้นทุนรวมทั้งหมด
total_cost = cost_price + fee_amount + ads_budget + shipping_cost + vat_amount

# 4. กำไรสุทธิ
net_profit = selling_price - total_cost
net_profit_margin = (net_profit / selling_price) * 100 if selling_price > 0 else 0

# --- 5. RESULT (แสดงผลง่ายๆ) ---
st.markdown("---")
st.subheader("🏁 สรุป: ขายชิ้นนี้...เหลือเงินกี่บาท?")

if net_profit > 0:
    st.markdown(f'<p class="big-money">+{net_profit:,.2f} บาท</p>', unsafe_allow_html=True)
    st.success(f"🎉 รอด! กำไร {net_profit_margin:.1f}% (เข้ากระเป๋าจริง)")
else:
    st.markdown(f'<p class="big-loss">{net_profit:,.2f} บาท</p>', unsafe_allow_html=True)
    st.error("😱 ขาดทุน! ขายดีแค่ไหนก็เจ๊ง หยุดขายหรือขึ้นราคาด่วน")

# --- 6. BREAKDOWN (ปุ่มดูไส้ใน) ---
with st.expander("🔍 เงินขาย 100% หายไปไหนบ้าง? (คลิกดู)"):
    # Data Visualization
    data = {
        'รายการ': ['ต้นทุนของ', 'ค่าธรรมเนียม Platform', 'ค่าแอด', 'ภาษี (VAT)', 'ค่าส่ง', 'กำไรเหลือจริง'],
        'จำนวนเงิน': [cost_price, fee_amount, ads_budget, vat_amount, shipping_cost, net_profit]
    }
    df = pd.DataFrame(data)
    
    # แสดงเป็นตารางสวยๆ
    st.table(df)
    
    st.caption("*หมายเหตุ: การคำนวณนี้เป็นการประมาณการเบื้องต้น (รวม VAT ในค่าธรรมเนียมแล้ว)")

# --- 7. FEATURE: PROMOTION SIMULATOR (ฟีเจอร์แถมที่โคตรคุ้ม) ---
st.markdown("---")
st.header("⚡ ลองจัดโปรฯ (Flash Sale)")
st.write("ถ้าร่วมแคมเปญ ลดราคาหนักๆ จะยังเหลือกำไรไหม?")

discount_percent = st.slider("จะลดราคากี่ %", 0, 50, 10)
new_price = selling_price * (100 - discount_percent) / 100

# คำนวณใหม่แบบไวๆ
new_fee = new_price * (platform_fee_percent / 100)
# สมมติ VAT แปรผันตามราคาใหม่
if has_vat:
    new_vat = new_price - (new_price * 100 / 107)
else:
    new_vat = 0
    
new_profit = new_price - (cost_price + new_fee + ads_budget + shipping_cost + new_vat)

col_sim1, col_sim2 = st.columns(2)
with col_sim1:
    st.metric("ราคาขายใหม่", f"{new_price:,.0f} บาท")
with col_sim2:
    st.metric("กำไรหลังลดราคา", f"{new_profit:,.2f} บาท", 
             delta_color="normal" if new_profit > 0 else "inverse")

if new_profit < 0:
    st.warning("⚠️ ลดขนาดนี้ เข้าเนื้อนะครับ!")
else:
    st.info("✅ ลดได้ครับ ยังเหลือกำไรอยู่")
