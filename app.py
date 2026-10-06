import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os
import time  # 💡 ఎర్రర్ వస్తే కాసేపు ఆగడానికి

# 1. పేజీ కాన్ఫిగరేషన్ మరియు స్టైలింగ్
st.set_page_config(page_title="Google Flow - AI Creative Studio", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    body { background-color: #0F0F0F; color: #FFFFFF; }
    .stApp { background-color: #0F0F0F; }
    div.stButton > button:first-child { background-color: #333333; color: white; border-radius: 10px; border: 1px solid #444; }
    .card { background-color: #1E1E1E; padding: 15px; border-radius: 12px; border: 1px solid #2D2D2D; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. సైడ్‌బార్
st.sidebar.title("Google Flow 🎬")
st.sidebar.caption("AI Creative Studio")
st.sidebar.write("---")

menu_choice = st.sidebar.radio("Explore Tools", ["📁 All Media", "👤 Characters", "🌄 Scenes", "🛠️ Tools"])
st.sidebar.write("---")
st.sidebar.subheader("👤 మీ ప్రొఫైల్")
st.sidebar.info("🪙 1,050 Google Flow Credits Available")
api_key = st.sidebar.text_input("Gemini API Key ఇవ్వండి:", type="password")

if not api_key:
    st.warning("⚠️ యాప్ రన్ అవ్వడానికి సైడ్‌బార్‌లో మీ Gemini API Key ని ఎంటర్ చేయండి.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.8-flash")

    if "project_step" not in st.session_state:
        st.session_state.project_step = "dashboard"
    if "selected_char" not in st.session_state:
        st.session_state.selected_char = "None"

    if menu_choice == "📁 All Media":
        st.title("📁 My Creations & Dashboard")
        if st.button("➕ New Project (కొత్త ప్రాజెక్ట్ ప్రారంభించు)", use_container_width=True):
            st.session_state.project_step = "create"
            st.rerun()
    else:
        st.session_state.project_step = "create"

    # ==================== PROJECT CREATION FLOW ====================
    if st.session_state.project_step == "create":
        st.title("🎬 AI Creative Studio - Project Flow")
        
        user_prompt = st.text_area("మీ స్టోరీ లేదా ప్రాంప్ట్ రాయండి:", placeholder="ఇక్కడ టైప్ చేయండి...")
        uploaded_file = st.file_uploader("క్యారెక్టర్ లేదా సీన్ ఇమేజ్ అప్‌లోడ్ చేయండి:", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="అప్‌లోడ్ చేసిన ఇమేజ్", width=300)

        # జనరేట్ బటన్
        if st.button("Generate Audio & Video 🚀", use_container_width=True):
            if user_prompt.strip():
                with st.spinner("AI రెస్పాన్స్ తయారవుతోంది... ⏳"):
                    
                    full_prompt = [user_prompt]
                    if uploaded_file:
                        full_prompt.append(img)
                    
                    response_received = False
                    ai_text = ""
                    
                    # 💡 కోటా లిమిట్ (429 ఎర్రర్) హ్యాండిల్ చేయడానికి ట్రై-క్యాచ్ లాజిక్
                    try:
                        response = model.generate_content(full_prompt)
                        ai_text = response.text
                        response_received = True
                    except Exception as e:
                        if "429" in str(e):
                            st.warning("⚠️ గూగుల్ ఉచిత లిమిట్ (Quota) దాటిపోయింది! 15 సెకన్లు ఆగి ఆటోమేటిక్‌గా మళ్లీ ప్రయత్నిస్తున్నాము...")
                            time.sleep(16)  # 16 సెకన్లు వెయిట్ చేస్తుంది
                            try:
                                response = model.generate_content(full_prompt)
                                ai_text = response.text
                                response_received = True
                            except Exception as retry_error:
                                st.error("మళ్లీ ప్రయత్నించినా లిమిట్ ఎర్రర్ వచ్చింది. దయచేసి ఒక నిమిషం ఆగి బటన్ నొక్కండి.")
                        else:
                            st.error(f"ఎర్రర్ వచ్చింది: {e}")

                    # ఒకవేళ డేటా విజయవంతంగా వస్తే ఆడియో, వీడియో క్రియేట్ చేస్తుంది
                    if response_received and ai_text:
                        st.markdown("### 📝 Generated Script:")
                        st.write(ai_text)

                        # ఆడియో జనరేషన్
                        short_text = ai_text[:300]
                        tts_lang = 'te' if any(chr(0x0C00) <= c <= chr(0x0C7F) for c in short_text) else 'en'
                        tts = gTTS(text=short_text, lang=tts_lang)
                        audio_path = "flow_audio.mp3"
                        tts.save(audio_path)
                        
                        st.markdown("### 🔊 AI Voice-Over:")
                        st.audio(audio_path, format="audio/mp3")

                        # వీడియో జనరేషన్
                        video_path = "flow_video.mp4"
                        if uploaded_file:
                            img.save("temp_flow_img.jpg")
                            image_clip = ImageClip("temp_flow_img.jpg")
                        else:
                            image_clip = ImageClip(size=(720, 480), color=(15, 15, 15))
                        
                        audio_clip = AudioFileClip(audio_path)
                        video_clip = image_clip.set_audio(audio_clip).set_duration(audio_clip.duration)
                        video_clip.write_videofile(video_path, fps=10, codec="libx264", audio_codec="aac", logger=None)
                        
                        st.markdown("### 🎬 Final Video Output:")
                        st.video(video_path)
                        
                        audio_clip.close()
                        video_clip.close()
                        st.success("✨ ప్రాజెక్ట్ సక్సెస్ఫుల్‌గా పూర్తయింది!")
            else:
                st.warning("దయచేసి ప్రాంప్ట్ టైప్ చేయండి!")
