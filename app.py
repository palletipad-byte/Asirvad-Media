import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import tempfile

# 1. Page Configuration (ఇది ఎప్పుడూ మొదటి లైన్లోనే ఉండాలి)
st.set_page_config(
    page_title="ఆశీర్వాద్ AI - మల్టీమీడియా స్టూడియో",
    page_icon="🎬",
    layout="wide"
)

# Initialize Gemini API using Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # మోడల్ నేమ్ సరిగ్గా సెట్ చేయడం
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    api_ready = False

# App Header
st.title("🎬 ఆశీర్వాద్ AI - ఆల్-ఇన్-వన్ మల్టీమీడియా స్టూడియో")
st.write("స్టోరీలు, ఫోటో విశ్లేషణలు మరియు వాయిస్ ఓవర్లను సులభంగా సృష్టించుకోండి.")

if not api_ready:
    st.error("⚠️ Streamlit Secrets లో `GEMINI_API_KEY` సెట్ చేయబడి లేదు. దయచేసి సెట్టింగ్స్‌లో దీన్ని యాడ్ చేయండి.")
else:
    # Sidebar Menu
    st.sidebar.title("🌟 ఆశీర్వాద్ మెనూ")
    feature_choice = st.sidebar.selectbox("ఫ్యూచర్ ఎంచుకోండి:", [
        "🏠 హోమ్ & డ్యాష్‌బోర్డ్",
        "📝 Feature 1: AI స్టోరీస్ & స్క్రిప్ట్స్", 
        "🖼️ Feature 2: Google Flow విజువల్ స్టూడియో", 
        "🎙️ Feature 3: వాయిస్ ఓవర్ & ఆడియో"
    ])

    if feature_choice == "🏠 హోమ్ & డ్యాష్‌బోర్డ్":
        st.subheader("స్వాగతం, ఆశీర్వాదం గారు! 🙏")
        st.info("మీ ప్రాజెక్ట్‌ల కోసం అన్ని మల్టీమీడియా ఫీచర్లు ఇక్కడ అందుబాటులో ఉన్నాయి.")

    elif feature_choice == "📝 Feature 1: AI స్టోరీస్ & స్క్రిప్ట్స్":
        st.subheader("📝 క్రియేటివ్ స్టోరీ మరియు స్క్రిప్ట్ జనరేటర్")
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
                st.warning("దయచేసి ఏదైనా టెక్స్ట్ రాయండి.")

    elif feature_choice == "🖼️ Feature 2: Google Flow విజువల్ స్టూడియో":
        st.subheader("🖼️ Google Flow స్టైల్ ఫోటో & విజువల్ అనాలిసిస్")
        st.write("మీ ఫోటోలను అప్‌లోడ్ చేసి వాటిపై AI సహాయంతో విశ్లేషణ చేయండి మరియు స్క్రిప్ట్స్ తయారు చేసుకోండి.")
        
        uploaded_file = st.file_uploader("ఫోటో అప్‌లోడ్ చేయండి:", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="అప్‌లోడ్ చేసిన ఇమేజ్", use_column_width=True)
            
            user_query = st.text_input("ఈ ఫోటో గురించి AI ని ఏమి అడగాలనుకుంటున్నారు? (ఉదా: ఈ డిజైన్ గురించి వివరించండి)")
            
            if st.button("విజువల్ విశ్లేషించు"):
                if user_query:
                    with st.spinner("విశ్లేషిస్తోంది..."):
                        try:
                            response = model.generate_content([image, user_query])
                            st.success("విశ్లేషణ పూర్తి!")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"ఎర్రర్ ఏర్పడింది: {e}")
                else:
                    st.warning("దయచేసి సరైన ప్రశ్న ఇవ్వండి.")

    elif feature_choice == "🎙️ Feature 3: వాయిస్ ఓవర్ & ఆడియో":
        st.subheader("🎙️ టెక్స్ట్ నుండి వాయిస్ ఓవర్ (TTS)")
        tts_text = st.text_area("ఆడియోగా మార్చవలసిన టెక్స్ట్ ఇక్కడ రాయండి:")
        lang_choice = st.selectbox("భాషను ఎంచుకోండి:", ["te", "en", "hi"])

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

# Footer
st.markdown("---")
st.markdown("**Created with ❤️ by ఆశీర్వాదం | Powered by Google Gemini API**")
            
