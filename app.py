import streamlit as st
from google import genai
from streamlit_mic_recorder import mic_recorder

# 1. API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key nahi mili! Settings me GEMINI_API_KEY set karein.")
    st.stop()

# 2. Memory (Chat History) Initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. UI Setup
st.set_page_config(page_title="AI Study Partner v2", page_icon="🎙️")
st.title("📚 AI Study Partner v2.0")
st.sidebar.title("Settings")
exam_class = st.sidebar.selectbox("Class/Exam:", ["Class 10", "Class 12", "NDA", "Agniveer", "Other"])

# Chat history ko screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Voice Input (Mic)
st.write("---")
col1, col2 = st.columns([1, 4])
with col1:
    st.write("Voice Input:")
    audio = mic_recorder(start_prompt="🎤 Start", stop_prompt="🛑 Stop", key='recorder')

# Agar mic se kuch bola gaya ho
voice_text = ""
if audio:
    voice_text = audio['text']
    if voice_text:
        st.info(f"Aapne bola: {voice_text}")

# 5. Chat Input (Type or Voice)
prompt = st.chat_input("Apna sawal likhein ya mic use karein...")

# Agar voice_text hai toh use prompt bana dena
if voice_text and not prompt:
    prompt = voice_text

if prompt:
    # User ka sawal history me jodo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI ka jawab nikalna (Pichli baaton ke sath)
    with st.chat_message("assistant"):
        with st.spinner("AI soch raha hai..."):
            try:
                # Chat History ko AI ko bhejna
                full_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                system_instruction = f"You are a helpful tutor for {exam_class}. Context of previous chat: {full_context}"
                
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                    config={'system_instruction': system_instruction}
                )
                
                answer = response.text
                st.markdown(answer)
                # AI ka jawab history me jodo
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # FAQs Suggestion (Related Question button style)
                st.write("---")
                st.caption("Aap ye bhi pooch sakte hain:")
                st.button("Isko aur detail me samjhao", on_click=lambda: st.session_state.update({"follow_up": "Is topic ko aur detail me samjhao"}))
                
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar me reset button
if st.sidebar.button("Clear Chat Memory"):
    st.session_state.messages = []
    st.rerun()
