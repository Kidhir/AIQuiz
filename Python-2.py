import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- Gemini API Setup ---
GEMINI_API_KEY = "AIzaSyAmZt-Pa31lf6TAZ_8p3S6qT2L8dNi-S1c"  # INBUILT Key (example key for demonstration)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# --- App Title ---
st.set_page_config(page_title="AI Personality Quiz Generator", layout="centered")

st.title("✨ AI Personality Quiz Generator")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📝 Take Quiz", "🔮 Result", "📊 Fun Dashboard", "📢 Share Badge"])

# --- Session State Initialization ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = {}

if 'result' not in st.session_state:
    st.session_state.result = ""

# --- Questions ---
questions = {
    "What's your ideal weekend?": ["Reading 📚", "Adventure 🧗", "Gaming 🎮", "Chilling 😌"],
    "Pick a favorite color": ["Blue 💙", "Red ❤️", "Green 💚", "Yellow 💛"],
    "What's your go-to drink?": ["Coffee ☕", "Tea 🍵", "Juice 🧃", "Water 💧"],
    "Preferred work style": ["Teamwork 👥", "Solo 🔍", "Flexible ⏳", "Structured 🗂️"],
    "What drives you?": ["Creativity 🎨", "Success 💼", "Stability 🛠️", "Passion ❤️"],
}

# --- Tab 1: Take Quiz ---
with tab1:
    st.header("📝 Answer a few questions")

    with st.form("quiz_form"):
        for q, options in questions.items():
            st.session_state.quiz_data[q] = st.radio(q, options, key=q)
        submitted = st.form_submit_button("Submit 🚀")

    if submitted:
        answers = "\n".join([f"{q}: {a}" for q, a in st.session_state.quiz_data.items()])
        prompt = f"""
        Based on the following preferences, create a fun, creative personality profile with a title, a short description, 3 fun facts, and a catchy phrase for social sharing.

        Preferences:
        {answers}

        Format:
        **Title**: ...
        **Description**: ...
        **Fun Facts**:
        - ...
        - ...
        - ...
        **Catchy Badge Text**: ...
        """
        response = model.generate_content(prompt)
        st.session_state.result = response.text
        st.success("Quiz submitted! Check the next tabs for results 🎉")

# --- Tab 2: Personality Result ---
with tab2:
    st.header("🔮 Your Personality Profile")
    if st.session_state.result:
        st.markdown(st.session_state.result)
    else:
        st.info("Take the quiz first to view your results!")

# --- Tab 3: Fun Dashboard ---
with tab3:
    st.header("📊 Your Fun Personality Dashboard")
    if st.session_state.result:
        st.metric("✨ Personality Score", f"{len(st.session_state.result) % 100} / 100")
        st.success("🔥 You're on fire with your unique vibes!")
        st.markdown("🎉 **Emoji Mood Match**: " + " ".join([a[-2:] for a in st.session_state.quiz_data.values()]))
        st.markdown("💡 **Dashboard Tip**: Embrace your unique energy every day!")
    else:
        st.warning("Submit your quiz to unlock this dashboard.")

# --- Tab 4: Social Badge ---
with tab4:
    st.header("📢 Share Your Badge")
    if st.session_state.result:
        badge = st.session_state.result.split("**Catchy Badge Text**:")[-1].strip()
        st.code(badge, language='markdown')
        st.markdown(f"🌐 Copy and share your badge with the world: \n\n> {badge}")
    else:
        st.info("Generate your result first to get a social badge.")

# --- Optional Email Sending (extendable) ---
# You can add a "Send to Email" button and use Gemini to generate an email body too.
