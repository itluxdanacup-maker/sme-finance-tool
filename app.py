import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SME Master Tool", page_icon="💎", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stNumberInput > div > div > input { text-align: right; }
    .premium-box { background-color: #f0f8ff; padding: 20px; border-radius: 10px; border: 1px solid #007bff; }
    .result-card { padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }
    .safe { background-color: #d1e7dd; color: #0f5132; }
    .danger { background-color: #f8d7da; color: #842029; }
</style>
""", unsafe_allow_html=True)

st.title("💎 SME Master Tool: ครบเครื่องเรื่องกำไร")
st.caption("ระบบวิเคราะห์สุขภาพการเงิน & เครื่องมือคำนวณราคาขายแม่นยำ")

# --- 2. INPUT DATA (SIDEBAR) ---
with st.sidebar:
    st.header("📝 ข้อมูลพื้นฐาน")
    cash = st.number_input("เงินสดในมือ", 0, value=50000)
    receivables = st.number_input("เงินรอโอน", 0, value=20000)
    inventory_val = st.number_input("มูลค่าสต็อก (ทุน)", 0, value=100000)
    
    st.markdown("---")
    debt = st.number_input("หนี้ต้องจ่าย (30 วัน)", 0, value=30000)
    fixed_cost = st.number_input("ค่าใช้จ่ายคงที่", 0, value=25000)
    
    st.markdown("---")
    avg_sales = st.number_input("ยอดขายเฉลี่ย/เดือน", 0, value=150000)
    cogs_current = st.number_input("ต้นทุนสินค้าขาย (COGS)", 0, value=90000)

# --- 3. LOGIC (CORE) ---
liquid_assets = cash + receivables
obligations = debt + fixed_cost
runway = (liquid_assets - debt) / fixed_cost if fixed_cost > 0 else 99
burn_rate = fixed_cost

# --- 4. TABS INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🏥 ตรวจสุขภาพ (ฟรี)", "💎 คำนวณราคาขาย (Premium)", "📦 คำนวณสั่งของ (Premium)"])

# === TAB 1: HEALTH CHECK (FREE VERSION) ===
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("ผลตรวจสุขภาพธุรกิจ")
        if runway < 1:
            st.error(f"🚨 **อันตราย!** เงินสดไม่พอจ่ายหนี้ (Runway {runway:.1f} เดือน)")
        elif runway < 3:
            st.warning(f"⚠️ **เฝ้าระวัง** เงินสดพอหมุนได้ {runway:.1f} เดือน")
        else:
            st.success(f"✅ **แข็งแรง** สภาพคล่องดีเยี่ยม (Runway {runway:.1f} เดือน)")
            
        # Basic Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("เงินสดสุทธิ", f"{liquid_assets - debt:,.0f}")
        m2.metric("กำไรขั้นต้น (บาท)", f"{avg_sales - cogs_current:,.0f}")
        m3.metric("Margin (%)", f"{(avg_sales - cogs_current)/avg_sales*100:.1f}%" if avg_sales > 0 else "0%")

    with col2:
        # Pie Chart
        fig = go.Figure(data=[go.Pie(labels=['เงินสดที่มี', 'หนี้ที่ต้องจ่าย'], values=[liquid_assets, obligations], hole=.3)])
        fig.update_layout(height=250, margin=dict(l=20,r=20,t=20,b=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# === TAB 2: SMART PRICING (KILLER FEATURE) ===
with tab2:
    st.markdown("""
    <div class="premium-box">
    <h3>💰 Reverse Pricing Calculator</h3>
    <p>อย่าตั้งราคาตามใจฉัน! คำนวณย้อนกลับเพื่อหากำไรสุทธิที่แท้จริง (รวมค่าธรรมเนียม Platform แล้ว)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("##### 1. ต้นทุนของคุณ")
        unit_cost = st.number_input("ต้นทุนสินค้าต่อชิ้น (รวมแพ็ค)", 0.0, value=950.0, step=10.0)
        target_profit = st.number_input("กำไรสุทธิที่อยากได้ (บาท/ชิ้น)", 0.0, value=300.0, step=10.0)
        
    with col_p2:
        st.markdown("##### 2. ค่าหัวคิว & ค่าใช้จ่ายแฝง")
        platform_fee = st.number_input("ค่าธรรมเนียม Platform (%)", 0.0, value=12.0, help="เช่น Shopee/Lazada รวม VAT (ประมาณ 10-15%)")
        ads_percent = st.number_input("เผื่อค่าโฆษณา (%)", 0.0, value=15.0)
        tax_vat = st.number_input("ภาษีมูลค่าเพิ่ม (VAT 7%)", 0.0, value=7.0, help="ถ้าจด VAT ให้ใส่ 7 ถ้าไม่จดใส่ 0")

    st.markdown("---")
    
    # Calculation Logic
    # Price = (Cost + Profit) / (1 - (Fee% + Ads% + Vat%)) 
    # *Note: สูตรนี้คิดแบบคร่าวๆ เพื่อ Cover ต้นทุน (สูตรจริง VAT จะคิดซ้อนยอดขาย แต่เพื่อความง่ายใช้การบวก % ไปก่อน)
    
    total_deduct_percent = platform_fee + ads_percent + (tax_vat if tax_vat > 0 else 0)
    
    if total_deduct_percent >= 100:
        st.error("เป็นไปไม่ได้! ค่าใช้จ่ายเกิน 100% ของราคาขาย")
        suggested_price = 0
    else:
        # สูตร Reverse Price: เราต้องการเงิน (Cost + Profit) เหลือถึงมือ ดังนั้นเราต้องตั้งราคาเผื่อโดนหัก %
        suggested_price = (unit_cost + target_profit) / ((100 - total_deduct_percent) / 100)
    
    col_res1, col_res2 = st.columns([1.5, 1])
    
    with col_res1:
        st.markdown(f"### 🏷️ ราคาที่ต้องตั้งขายคือ: <span style='color:#007bff; font-size:36px'> {suggested_price:,.0f} </span> บาท", unsafe_allow_html=True)
        st.caption(f"เพื่อให้เหลือเข้ากระเป๋าจริง {target_profit:,.0f} บาท/ชิ้น")
        
    with col_res2:
        # Breakdown chart
        fee_amt = suggested_price * (platform_fee/100)
        ads_amt = suggested_price * (ads_percent/100)
        vat_amt = suggested_price * (tax_vat/100)
        
        df_price = pd.DataFrame({
            'รายการ': ['ต้นทุนของ', 'กำไรเข้ากระเป๋า', 'จ่าย Platform', 'จ่ายค่าแอด', 'ภาษี'],
            'จำนวนเงิน': [unit_cost, target_profit, fee_amt, ads_amt, vat_amt]
        })
        st.dataframe(df_price, hide_index=True)

# === TAB 3: SMART RESTOCK (INVENTORY) ===
with tab3:
    st.markdown("""
    <div class="premium-box">
    <h3>📦 Smart Restock Alert</h3>
    <p>ของจะหมดวันไหน? ต้องสั่งเพิ่มเมื่อไหร่? (คำนวณเผื่อเวลาขนส่งให้แล้ว)</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    current_stock = c1.number_input("สต็อกปัจจุบัน (ชิ้น)", 0, value=100)
    sales_velocity = c2.number_input("ขายออกเฉลี่ย (ชิ้น/วัน)", 0, value=5)
    lead_time = c3.number_input("ระยะเวลาขนส่ง (วัน)", 0, value=15, help="สั่งของจากจีน/โรงงาน ใช้เวลากี่วันกว่าของจะถึงมือ")
    
    # Logic
    if sales_velocity > 0:
        days_left = current_stock / sales_velocity
        reorder_point = sales_velocity * lead_time # จุดที่ต้องสั่งของ (Simple Reorder Point)
        stock_status = ""
        
        st.markdown(f"##### 📊 สถานะสต็อก: ขายได้อีก **{days_left:.0f}** วัน")
        
        # Timeline Visualization
        my_bar = st.progress(0)
        if days_left <= lead_time:
            st.error(f"🚨 **สั่งของด่วน!** (เหลือเวลาขาย {days_left:.0f} วัน แต่ของใช้เวลาส่ง {lead_time} วัน -> ของขาดแน่นอน!)")
            my_bar.progress(100)
        elif days_left <= (lead_time + 7):
            st.warning(f"⚠️ **เตรียมสั่งได้แล้ว** (เหลือ Buffer อีก {(days_left - lead_time):.0f} วัน)")
            my_bar.progress(70)
        else:
            st.success(f"✅ **ยังปลอดภัย** อีก {(days_left - lead_time):.0f} วันค่อยสั่งก็ได้")
            my_bar.progress(30)
            
        st.info(f"💡 **Tip:** ควรเริ่มกดสั่งของเมื่อสต็อกเหลือต่ำกว่า **{reorder_point}** ชิ้น")
        
    else:
        st.write("กรุณากรอกยอดขายต่อวัน")
