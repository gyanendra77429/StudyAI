import streamlit as st
from google import genai
from streamlit_mic_recorder import speech_to_text

# ==========================================
# 🎯 DEVELOPER BRANDING
DEVELOPER_NAME = "Gyanendra Singh" 
# ==========================================

# 1. API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key nahi mili! Settings me GEMINI_API_KEY set karein.")
    st.stop()

# 2. Memory (Chat History) Initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. UI Setup & Branding
st.set_page_config(page_title=f"AI Study Partner by {DEVELOPER_NAME}", page_icon="📚")
st.title("📚 AI Study Partner v2.0")

# --- SIDEBAR: OPTIONS & PROMOTION ---
st.sidebar.title("⚙️ Study Options")

exam_class = st.sidebar.selectbox(
    "Aap kis exam ki taiyari kar rahe hain?", 
    ["Class 10", "Class 12", "NDA", "Agniveer", "Air Force", "Other"]
)

style = st.sidebar.selectbox(
    "Aapko jawab kis tarike se chahiye?", 
    [
        "Easy Explanation (Bilkul aasan bhasha me)", 
        "Short Notes (To-the-point bullet points)", 
        "Step-by-Step Solution (Maths/Science ke liye)", 
        "Exam Oriented (Important Questions & Answers)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Developer Profile")
st.sidebar.success(f"**Created by: {DEVELOPER_NAME}**")
st.sidebar.info("🚀 Powered by Gemini AI & Streamlit")

if st.sidebar.button("Clear Chat Memory"):
    st.session_state.messages = []
    st.rerun()
# -------------------------------------

# Chat history ko screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Voice Input 
st.write("---")
col1, col2 = st.columns([1, 4])
with col1:
    st.write("Voice Input:")
    voice_text = speech_to_text(start_prompt="🎤 Start", stop_prompt="🛑 Stop", language='hi', key='recorder')

if voice_text:
    st.info(f"🎤 Aapne bola: {voice_text}")

# 5. Chat Input (Type or Voice)
prompt = st.chat_input("Apna sawal likhein ya mic use karein...")

if voice_text and not prompt:
    prompt = voice_text

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI soch raha hai..."):
            try:
                full_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                
                # 🔥 YAHAN HUMNE AI KO SPECIALLY INSTRUCT KIYA HAI KI WEIRD CODES NA BHEJE
                system_instruction = (
                    f"You are an expert tutor. The student is preparing for: {exam_class}. "
                    f"They want the response in this style: {style}. "
                    f"Answer the question clearly. Use friendly Hinglish/Hindi mixed language. \n\n"
                    f"CRITICAL RULES FOR FORMULAS:\n"
                    f"1. DO NOT use complex LaTeX formatting or special delimiters like $$, \[, \], or $. \n"
                    f"2. Write ALL physics and math formulas in simple plain text (e.g., write E = mc^2, v = u + at, F = g*(m1*m2)/r^2) so it reads naturally without any format breaks.\n"
                    f"3. Keep important laws or terms bolded using standard **text** format.\n\n"
                    f"Context of previous chat: {full_context}"
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config={'system_instruction': system_instruction}
                )
                
                answer = response.text
                st.markdown(answer)
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                st.write("---")
                st.caption("💡 Aap isi jawab se related koi bhi follow-up sawal niche type karke ya bolkar pooch sakte hain!")
                
            except Exception as e:
                st.error(f"Error: {e}")

# --- FOOTER PROMOTION ---
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 14px;'>Made with ❤️ by <b>{DEVELOPER_NAME}</b> | © 2026 All Rights Reserved</p>", 
    unsafe_allow_html=True
)
