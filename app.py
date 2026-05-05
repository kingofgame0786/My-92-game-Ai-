import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="92Jeeto AI Master", layout="centered")

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

st.title("🤖 92Jeeto اسمارٹ AI اینالائزر")

file = st.file_uploader("ہسٹری کا اسکرین شاٹ اپلوڈ کریں", type=["jpg", "png", "jpeg"])

def advanced_logic(history):
    # ہسٹری کو ترتیب دینا (تازہ ترین سے پرانی)
    if not history: return "انتظار", 0
    
    last_val = history[0]
    count_last = 0
    for x in history:
        if x == last_val: count_last += 1
        else: break
    
    # 1. ڈریگن ٹرینڈ (اگر مسلسل 4 یا زیادہ بار آئے)
    if count_last >= 4:
        return last_val, 95  # ڈریگن کے ساتھ چلیں
    
    # 2. جمپ پیٹرن (B-S-B-S)
    if len(history) >= 4:
        if history[0] != history[1] and history[1] != history[2]:
            decision = "BIG" if last_val == "SMALL" else "SMALL"
            return decision, 85
            
    # 3. بریک آؤٹ لاجک (لمبے سلسلے کے بعد تبدیلی)
    if count_last == 1 and len(history) >= 5:
        # اگر اس سے پہلے 4 بار مخالف چیز آئی تھی
        prev_val = history[1]
        prev_count = 0
        for x in history[1:]:
            if x == prev_val: prev_count += 1
            else: break
        if prev_count >= 4:
            return last_val, 80 # نئے ٹرینڈ کے ساتھ چلیں

    # 4. ڈیفالٹ (مخالف چال)
    decision = "BIG" if last_val == "SMALL" else "SMALL"
    return decision, 65

if file:
    img = Image.open(file)
    st.image(img, width=300)
    
    if st.button("AI تجزیہ شروع کریں"):
        with st.spinner("ڈیٹا کا گہرا تجزیہ جاری ہے..."):
            result = reader.readtext(np.array(img), detail=0)
            # ڈیٹا کو فلٹر کرنا
            history = [t.upper() for t in result if "BIG" in t.upper() or "SMALL" in t.upper()]
            
            if len(history) >= 2:
                st.write(f"📋 اسکین شدہ ہسٹری: {', '.join(history[:6])}")
                
                prediction, confidence = advanced_logic(history)
                
                st.markdown("---")
                st.subheader("🎯 AI کا حتمی فیصلہ:")
                
                if prediction == "BIG":
                    st.success(f"✅ اگلی چال: **{prediction}**")
                else:
                    st.error(f"✅ اگلی چال: **{prediction}**")
                
                st.metric("یقین کی حد (Confidence)", f"{confidence}%")
                
                if confidence < 70:
                    st.warning("⚠️ محتاط رہیں: پیٹرن واضح نہیں ہے۔")
            else:
                st.error("ڈیٹا صحیح اسکین نہیں ہوا۔ براہ کرم صاف تصویر اپلوڈ کریں۔")

st.sidebar.info("ٹپ: تصویر ایسی لیں جس میں 'Period' اور 'Big/Small' دونوں صاف نظر آئیں۔")
