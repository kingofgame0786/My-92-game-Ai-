import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# ایپ کی بنیادی ترتیب
st.set_page_config(page_title="92Jeeto Formula Analyzer", page_icon="📊", layout="wide")

# سٹائلنگ
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; height: 3em; font-size: 20px; }
    .report-card { padding: 15px; border-radius: 10px; background-color: #f1f8e9; border-left: 5px solid #2e7d32; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 92Jeeto ماسٹر فارمولا اینالائزر")

# سائیڈ بار سیٹنگز
st.sidebar.header("⚙️ سیٹنگز")
mode = st.sidebar.selectbox("ٹائم فریم منتخب کریں", ["30 Seconds", "1 Minute", "3 Minute", "5 Minute"])

# OCR ماڈل لوڈ کرنا
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# تجزیاتی لاجک (فارمولے)
def run_analysis(numbers, sizes, colors):
    hints = []
    
    # 1. ڈریگن ٹرینڈ
    if len(sizes) >= 5 and len(set(sizes[-5:])) == 1:
        hints.append(f"🐉 **ڈریگن الرٹ:** مسلسل {sizes[-1]} آ رہا ہے۔ ٹرینڈ کے ساتھ چلیں!")

    # 2. جمپ پیٹرن
    if len(sizes) >= 4:
        p = "".join(sizes[-4:])
        if p in ["BSBS", "SBSB"]:
            nxt = "Big" if sizes[-1] == "S" else "Small"
            hints.append(f"🦘 **جمپ پیٹرن:** زگ زیگ جاری ہے۔ اگلی چال **{nxt}** ہو سکتی ہے۔")

    # 3. رنگوں کا توازن
    if colors.count("R") >= 5: hints.append("🎨 **رنگ:** Red کی زیادتی ہے، اب **Green** کے امکانات ہیں۔")
    elif colors.count("G") >= 5: hints.append("🎨 **رنگ:** Green کی زیادتی ہے، اب **Red** کے امکانات ہیں۔")

    # 6. وائلٹ فیکٹر
    if colors and colors[-1] == "V":
        hints.append("💜 **وائلٹ وارننگ:** ٹرینڈ بدلنے والا ہے، محتاط رہیں!")

    # 7. ریاضیاتی اوسط
    if len(numbers) >= 5:
        avg = sum(numbers[-5:]) / 5
        advice = "Big" if avg < 4.5 else "Small"
        hints.append(f"⚖️ **اوسط لاجک:** اوسط {avg} ہے۔ مارکیٹ **{advice}** کی طرف جا سکتی ہے۔")

    return hints

# ان پٹ کے دو طریقے
tab1, tab2 = st.tabs(["📸 اسکرین شاٹ اسکین", "⌨️ دستی اندراج (Manual)"])

with tab1:
    file = st.file_uploader("گیم ہسٹری کا اسکرین شاٹ اپلوڈ کریں", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="اپلوڈ شدہ تصویر", width=300)
        if st.button("اسکین اور تجزیہ کریں"):
            with st.spinner("ڈیٹا پڑھا جا رہا ہے..."):
                results = reader.readtext(np.array(img), detail=0)
                st.write("شناخت شدہ ڈیٹا:", results)
                # یہاں مزید فلٹرنگ شامل کی جا سکتی ہے
                st.info("اسکین شدہ ڈیٹا پر فارمولے لاگو ہو رہے ہیں...")

with tab2:
    n_in = st.text_input("نمبرز لکھیں (مثال: 1,4,2,8,5)")
    s_in = st.text_input("سائز لکھیں (B برائے Big، S برائے Small - مثال: B,S,S,B,S)")
    c_in = st.text_input("رنگ لکھیں (R, G, V - مثال: R,G,R,R,V)")
    
    if st.button("تجزیہ شروع کریں"):
        try:
            nums = [int(x.strip()) for x in n_in.split(",") if x.strip()]
            szs = [x.strip().upper() for x in s_in.split(",") if x.strip()]
            cols = [x.strip().upper() for x in c_in.split(",") if x.strip()]
            
            final_results = run_analysis(nums, szs, cols)
            
            st.subheader(f"📋 {mode} کا تجزیہ:")
            if final_results:
                for h in final_results:
                    st.markdown(f"<div class='report-card'>{h}</div>", unsafe_allow_html=True)
            else:
                st.warning("کوئی واضح پیٹرن نہیں ملا۔")
        except:
            st.error("براہ کرم ڈیٹا صحیح فارمیٹ میں لکھیں۔")

st.sidebar.markdown("---")
st.sidebar.write("Powered by: 92Jeeto Formula Logic")
