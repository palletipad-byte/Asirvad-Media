import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import tempfile

# Page Configuration
st.set_page_config(
    page_title="Asirvad-Media",
    page_icon="🎬",
    layout="wide"
)

# Initialize Gemini API using Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    api_ready = True
except Exception as e:
    api_ready = False

st.title("🎬 ఆశీర్వాద్ AI - మల్టీమీడియా క్రియేటర్")
st.write("స్టోరీలు, వాయిస్ ఓవర్స్ మరియు కంటెంట్‌ను ఇక్కడ నేరుగా క్రియేట్ చేసుకోండి.")

if not api_ready:
    st.error("⚠️ Streamlit Secrets లో `GEMINI_API_KEY` సెట్ చేయబడి లేదు. దయచేసి సెట్టింగ్స్‌లో దీన్ని యాడ్ చేయండి.")
else:
    # Tabs for different features
    tab1, tab2, tab3 = st.tabs(["📝 AI స్టోరీస్", "🎙️️ వాయిస్ ఓవర్ (TTS)", "ℹ️ గురించి"])

    with tab1:
        st.subheader("క్రియేటివ్ స్టోరీ మరియు స్క్రిప్ట్ జనరేటర్")
        prompt = st.text_area("మీకు కావలసిన టాపిక్ లేదా ఐడియా ఇక్కడ రాయండి:")
        
        if st.button("స్టోరీ జనరేట్ చేయు"):
            if prompt:
                with st.spinner("జనరేట్ అవుతోంది..."):
                    try:
                        response = model.generate_content(prompt)
                        st.success("విజయవంతంగా జనరేట్ చేయబడింది!")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"ఎర్రర్ ఏర్పడింది: {e}")
            else:
                st.warning("దయచేసి ఏదെങ്കിലും టెక్స్ట్ రాయండి.")

    with tab2:
        st.subheader("టెక్స్ట్ నుండి వాయిస్ ఓవర్ (gTTS)")
        tts_text = st.text_area("ఆడియోగా మార్చవలసిన టెక్స్ట్ ఇక్కడ రాయండి:")
        lang_choice = st.selectbox("భాషను ఎంచుకోండి (Language):", ["te", "en", "hi"])

        if st.button("వాయిస్ క్రియేట్ చేయు"):
            if tts_text:
                with st.spinner("ఆడియో తయారవుతోంది..."):
                    try:
                        tts = gTTS(text=tts_text, lang=lang_choice)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            temp_path = fp.name
                            tts.save(temp_path)
                        
                        st.audio(temp_path, format="audio/mp3")
                        st.success("వాయిస్ ఓవర్ సిద్ధంగా ఉంది!")
                    except Exception as e:
                        st.error(f"ఎర్రర్ ఏర్పడింది: {e}")
            else:
                st.warning("దయచేసి టెక్స్ట్ ఎంటర్ చేయండి.")

    with tab3:
        st.subheader("ఆశీర్వాద్ మీడియా గురించి")
        st.write("ఈ అప్లికేషన్ సృష్టికర్తలు మరియు డెవలపర్ల కోసం ప్రత్యేకంగా రూపొందించబడింది.")
        st.markdown("**Created with ❤️️ by ఆశీర్వాదం**")
                        
