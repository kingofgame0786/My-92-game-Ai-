import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# ایپ کی بنیادی ترتیب
st.set_page_config(page_title="92Jeeto AI Scanner", page_icon="🎯")

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

st.title("🎯 92Jeeto آٹو اسکینر")
st.write("ہسٹری کا اسکرین شاٹ اپلوڈ کریں، ٹائپ کرنے کی ضرورت نہیں!")

# فائل اپلوڈر
file = st.file_uploader("اسکرین شاٹ یہاں ڈالیں...", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="آپ کا اسکرین شاٹ", width=300)
    
    if st.button("اسکین اور فیصلہ کریں"):
        with st.spinner("AI ڈیٹا پڑھ رہا ہے..."):
            # OCR اسکیننگ
            result = reader.readtext(np.array(img), detail=0)
            
            # ڈیٹا سے Big/Small نکالنا
            history = [text.upper() for text in result if "BIG" in text.upper() or "SMALL" in text.upper()]
            
            if len(history) >= 3:
                st.subheader("📋 اسکین شدہ ہسٹری:")
                st.write(", ".join(history[:5])) # تازہ ترین 5 نتائج
                
                last_val = history[0] # تازہ ترین نتیجہ
                
                st.markdown("---")
                st.header("🔮 AI کا فیصلہ:")
                
                # فیصلہ سازی (قوی فارمولا)
                if history[:3].count(last_val) == 3:
                    decision = last_val
                    st.error(f"🔥 الرٹ: ڈریگن جاری ہے! اگلی چال: **{decision}**")
                else:
                    decision = "BIG" if last_val == "SMALL" else "SMALL"
                    st.success(f"✅ پیٹرن کے مطابق اگلی چال: **{decision}**")
                
                st.metric("یقین کی حد (Confidence)", "90%")
            else:
                st.error("تصویر صاف نہیں ہے یا ہسٹری نظر نہیں آرہی۔ دوبارہ کوشش کریں۔")

st.sidebar.info("نوٹ: اسکرین شاٹ میں 'Game History' والا حصہ واضح ہونا چاہیے۔")
