import streamlit as st
import google.generativeai as genai

# 1. API Key ko safe tarike se check karna
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key nahi mili! Kripya Streamlit ke Advanced Settings me GEMINI_API_KEY set karein.")
    st.stop()

# 2. App ka Interface (Look) design karna
st.set_page_config(page_title="AI Study Partner", page_icon="📚", layout="centered")

st.title("📚 Custom AI Study Partner")
st.write("Apni class/exam aur answer ka tarika chunein, fir sawal poochein!")

# Student ke liye options
exam_class = st.selectbox(
    "Aap kis class ya exam ki taiyari kar rahe hain?", 
    ["Class 10", "Class 12", "NDA", "Agniveer", "Air Force", "Other Competitive Exam"]
)

style = st.selectbox(
    "Aapko jawab kis tarike se chahiye?", 
    [
        "Easy Explanation (Bilkul aasan bhasha me)", 
        "Short Notes (To-the-point bullet points)", 
        "Step-by-Step Solution (Maths/Science ke liye)", 
        "Exam Oriented (Important Questions & Answers)"
    ]
)

# Sawal likhne ki jagah
user_question = st.text_area("Apna sawal ya topic yahan likhein:", placeholder="Example: Photosynthesis kya hai? ya English Grammar ke rules...")

# Button aur AI ka kaam
if st.button("Jawab Dekho ✨", use_container_width=True):
    if user_question:
        with st.spinner("AI aapke liye jawab taiyar kar raha hai..."):
            try:
                # Gemini ka sabse latest fast free model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # AI ko samjhana ki use kaise jawab dena hai
                prompt = (
                    f"You are an expert tutor. The student is preparing for: {exam_class}. "
                    f"They want the response in this style: {style}. "
                    f"Answer the following question clearly. Use friendly Hinglish/Hindi mixed language "
                    f"so it's easy to understand. Keep formulas and important terms highlighted. \n\n"
                    f"Question: {user_question}"
                )
                
                response = model.generate_content(prompt)
                
                # Jawab screen par dikhana
                st.success("🤖 AI Ka Jawab:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Kuch galti hui: {e}")
    else:
        st.warning("Kripya pehle apna sawal type karein!")
