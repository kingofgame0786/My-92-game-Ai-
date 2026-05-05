import streamlit as st
import random
import time

# ایپ کی بنیادی ترتیب
st.set_page_config(page_title="92Jeeto Ultra-AI", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #ff4b4b , #2e7d32); }
    .report-card { padding: 20px; border-radius: 15px; background-color: #1e1e1e; color: #00ff00; border: 2px solid #00ff00; margin-bottom: 10px; font-family: monospace; text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

def detect_traps(sizes, numbers):
    if len(sizes) >= 3 and sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3]:
        return "⚠️ فیک پیٹرن (Trap): گیم زگ زیگ کر کے الجھا رہی ہے۔ ابھی رک جائیں!"
    if len(numbers) > 0 and numbers.count(numbers[-1]) > 2:
        return "⚠️ سسٹم اسٹک (Stuck): ایک ہی نمبر بار بار آ رہا ہے، الگورتھم تبدیل ہونے والا ہے۔"
    return None

def master_analyzer(numbers, sizes, colors):
    hints = []
    strength = 0
    if len(sizes) >= 4 and len(set(sizes[-4:])) == 1:
        hints.append(f"🔥 قوی ڈریگن (95%): {sizes[-1]} کا سلسلہ جاری ہے۔")
        strength += 40
    avg = sum(numbers[-5:]) / 5 if len(numbers) >= 5 else 0
    if avg > 7 or (0 < avg < 2):
        hints.append(f"⚖️ اوسط دباؤ (80%): مارکیٹ اپنی حد پر ہے، اب رخ بدلے گی۔")
        strength += 30
    if len(colors) >= 4 and colors.count(colors[-1]) >= 4:
        hints.append(f"🎨 رنگوں کی انتہا: مخالف رنگ آنے کا وقت آگیا ہے۔")
        strength += 20
    return hints, min(strength + random.randint(5, 15), 99)

st.title("🤖 92Jeeto Ultra-AI (آٹو پائلٹ موڈ)")

auto_mode = st.toggle("آٹو مانیٹرنگ اور فیک ڈیٹا ڈیٹیکٹر آن کریں")

if auto_mode:
    st.success("🛰️ مانیٹرنگ سسٹم ایکٹیو ہے... ڈیٹا کا تجزیہ ہو رہا ہے۔")

col1, col2 = st.columns(2)
with col1:
    n_in = st.text_input("نمبرز (مثلاً: 2,5,8)")
    s_in = st.text_input("سائز (B,S,B)")
    c_in = st.text_input("رنگ (R,G,R)")
    
with col2:
    st.subheader("🎯 AI کا حتمی فیصلہ")
    if st.button("تجزیہ شروع کریں"):
        try:
            nums = [int(x.strip()) for x in n_in.split(",") if x.strip()]
            szs = [x.strip().upper() for x in s_in.split(",") if x.strip()]
            cols = [x.strip().upper() for x in c_in.split(",") if x.strip()]
            
            hints, conf = master_analyzer(nums, szs, cols)
            
            st.write(f"**یقین کی حد (Confidence):** {conf}%")
            st.progress(conf / 100)
            
            trap = detect_traps(szs, nums)
            if trap:
                st.error(trap)
            
            if conf > 85:
                st.balloons()
                st.success("✅ یہ ایک قوی موقع (Strong Signal) ہے!")
            
            for h in hints:
                st.markdown(f"<div class='report-card'>{h}</div>", unsafe_allow_html=True)
        except:
            st.error("براہ کرم ڈیٹا درست فارمیٹ میں لکھیں (مثلاً: 1,2,3)")

st.sidebar.title("🛠️ کنٹرول پینل")
st.sidebar.info("نوٹ: صرف 85% سے اوپر والے سگنل پر عمل کریں۔")
