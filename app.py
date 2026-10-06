import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os

# 1. పేజీ కాన్ఫిగరేషన్ మరియు గూగుల్ ఫ్లో లాంటి డార్క్ థీమ్ స్టైలింగ్
st.set_page_config(page_title="Google Flow - AI Creative Studio", page_icon="🎬", layout="wide")

# కస్టమ్ CSS ద్వారా గూగుల్ ఫ్లో లాంటి డార్క్ స్క్రీన్ డిజైన్ చేయడం
st.markdown("""
    <style>
    body { background-color: #0F0F0F; color: #FFFFFF; }
    .stApp { background-color: #0F0F0F; }
    .sidebar .sidebar-content { background-color: #1A1A1A; }
    div.stButton > button:first-child { background-color: #333333; color: white; border-radius: 10px; border: 1px solid #444; }
    div.stButton > button:first-child:hover { background-color: #444444; border-color: #555; }
    .card { background-color: #1E1E1E; padding: 15px; border-radius: 12px; border: 1px solid #2D2D2D; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Streamlit Secrets నుండి నేరుగా API కీ కాన్ఫిగర్ చేయడం
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    api_ready = True
except Exception as e:
    api_ready = False

# 2. సైడ్‌బార్ కాన్ఫిగరేషన్ (గూగుల్ ఫ్లో లేఅవుట్ లాగా)
st.sidebar.title("Google Flow 🎬")
st.sidebar.caption("AI Creative Studio")
st.sidebar.write("---")

# సైడ్‌బార్ మెనూ ఆప్షన్స్
menu_choice = st.sidebar.radio(
    "Explore Tools",
    ["📁 All Media", "👤 Characters", "🌄 Scenes", "🛠️ Tools"]
)

st.sidebar.write("---")
st.sidebar.subheader("👤 మీ ప్రొఫైల్")
st.sidebar.info("🪙 1,050 Google Flow Credits Available")

if not api_ready:
    st.error("⚠️️ Streamlit Secrets లో `GEMINI_API_KEY` సెట్ చేయబడి లేదు. దయచేసి సెట్టింగ్స్‌లో దీన్ని యాడ్ చేయండి.")
else:
    # సెషన్ స్టేట్స్ సెటప్
    if "project_step" not in st.session_state:
        st.session_state.project_step = "dashboard"
    if "selected_char" not in st.session_state:
        st.session_state.selected_char = "None"

    # ==================== DASHBOARD / ALL MEDIA ====================
    if menu_choice == "📁 All Media":
        st.title("📁 My Creations & Dashboard")
        st.write("ఇక్కడ మీ పాత ప్రాజెక్ట్స్ మరియు కొత్త ప్రాజెక్ట్స్ మేనేజ్ చేయవచ్చు.")
        
        if st.button("➕ New Project (కొత్త ప్రాజెక్ట్ ప్రారంభించు)", use_container_width=True):
            st.session_state.project_step = "create"
            st.rerun()

        st.write("---")
        st.subheader("ఇటీవలి ప్రాజెక్ట్స్ (Recent Creations)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="card"><strong>Project_01.mp4</strong><br><p style="color:gray;">Sept 14 - 00:05</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card"><strong>Character_Pose.png</strong><br><p style="color:gray;">Sept 09 - 19:56</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="card"><strong>Scene_Audio.mp3</strong><br><p style="color:gray;">Sept 05 - 10:41</p></div>', unsafe_allow_html=True)

    # ==================== CHARACTERS MENU ====================
    elif menu_choice == "👤 Characters":
        st.title("👤 Build & Reuse Characters")
        st.write("వీడియోల కోసం కింద ఉన్న శాంపిల్ క్యారెక్టర్లలో ఒకదానిని ఎంచుకోండి:")
        
        char_cols = st.columns(3)
        with char_cols[0]:
            st.markdown('<div class="card"><strong>The Eccentric</strong><br><p style="color:gray;">Unforgettable quirky humans.</p></div>', unsafe_allow_html=True)
            if st.button("Select Eccentric"): st.session_state.selected_char = "The Eccentric"
        with char_cols[1]:
            st.markdown('<div class="card"><strong>The Professional</strong><br><p style="color:gray;">Clean cut, well spoken, competent.</p></div>', unsafe_allow_html=True)
            if st.button("Select Professional"): st.session_state.selected_char = "The Professional"
        with char_cols[2]:
            st.markdown('<div class="card"><strong>The Wildcard</strong><br><p style="color:gray;">Beyond human, anything can be character.</p></div>', unsafe_allow_html=True)
            if st.button("Select Wildcard"): st.session_state.selected_char = "The Wildcard"
            
        st.success(f"ప్రస్తుతం ఎంచుకున్న క్యారెక్టర్: **{st.session_state.selected_char}**")

    # ==================== SCENES / TOOLS (CREATION PROCESS) ====================
    else:
        st.session_state.project_step = "create"

    # ==================== NEW PROJECT CREATION FLOW ====================
    if st.session_state.project_step == "create":
        st.write("---")
        st.title("🎬 AI Creative Studio - Project Flow")
        st.write(f"🧬 యాక్టివ్ క్యారెక్టర్: **{st.session_state.selected_char}**")

        user_prompt = st.text_area("మీ స్టోరీ లేదా ప్రాంప్ట్ రాయండి (Describe your character/scene):", 
                                   placeholder="ఉదాహరణకు: ఈ క్యారెక్టర్ అడవిలో నడుస్తూ ఒక మ్యాజిక్ బాక్స్ చూసింది...")
        
        uploaded_file = st.file_uploader("క్యారెక్టర్ లేదా సీన్ ఇమేజ్ అప్‌‌లోడ్ చేయండి:", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="ప్రాజెక్ట్ ఇమేజ్", width=300)

        if st.button("Generate Audio & Video 🚀", use_container_width=True):
            if user_prompt.strip():
                with st.spinner("గూగుల్ ఫ్లో లాజిక్ ప్రకారం AI రెస్పాన్స్ మరియు ఆడియో/వీడియో ఫైల్స్ తయారవుతున్నాయి... ⏳"):
                    try:
                        full_prompt = [f"Character Style: {st.session_state.selected_char}. Prompt: {user_prompt}"]
                        if uploaded_file:
                            full_prompt.append(img)
                        
                        response = model.generate_content(full_prompt)
                        ai_text = response.text
                        
                        st.markdown("### 📝 Generated Script:")
                        st.write(ai_text)

                        short_text = ai_text[:300]
                        tts_lang = 'te' if any(chr(0x0C00) <= c <= chr(0x0C7F) for c in short_text) else 'en'
                        
                        tts = gTTS(text=short_text, lang=tts_lang)
                        audio_path = "flow_audio.mp3"
                        tts.save(audio_path)
                        
                        st.markdown("### 🔊 AI Voice-Over (Audio):")
                        st.audio(audio_path, format="audio/mp3")

                        st.markdown("### 🎬 Final Video Output:")
                        video_path = "flow_video.mp4"
                        
                        if uploaded_file:
                            img.save("temp_flow_img.jpg")
                            image_clip = ImageClip("temp_flow_img.jpg")
                        else:
                            image_clip = ImageClip(size=(720, 480), color=(15, 15, 15))
                        
                        audio_clip = AudioFileClip(audio_path)
                        video_clip = image_clip.set_audio(audio_clip).set_duration(audio_clip.duration)
                        
                        video_clip.write_videofile(video_path, fps=10, codec="libx264", audio_codec="aac", logger=None)
                        st.video(video_path)
                        
                        audio_clip.close()
                        video_clip.close()
                        st.success("✨ గూగుల్ ఫ్లో ప్రాజెక్ట్ సక్సెస్ఫుల్‌గా పూర్యయింది!")

                    except Exception as e:
                        st.error(f"ఎర్రర్ వచ్చింది: {e}")
            else:
                st.warning("దయచేసి మీ ప్రాజెక్ట్ కోసం కింద ఉన్న బాక్స్‌లో ఏదైనా ప్రాంప్ట్ టైప్ చేయండి!")
        
