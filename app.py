import streamlit as st
from video.script import split_script
from video.render import make_video

st.set_page_config(page_title="My AI Video Generator", page_icon="🎬", layout="wide")
st.title("🎬 My AI Video Generator")
st.caption("Script → scenes → video. Add your own model/API later for AI generation.")

tab1, tab2 = st.tabs(["📝 Script → Video", "🖼️ Photo → Video"])

with tab1:
    script = st.text_area("Enter your script", height=260,
        placeholder="Scene 1: A little girl walks through a sunny garden...\nScene 2: She sees a butterfly...")
    duration = st.slider("Target duration (minutes)", 1, 20, 1)
    fps = st.selectbox("FPS", [24, 30], index=0)
    if st.button("🎬 Create Video", type="primary"):
        if not script.strip():
            st.error("Please enter a script.")
        else:
            scenes = split_script(script, duration)
            with st.spinner("Creating video..."):
                output = make_video(scenes, duration, fps)
            st.success("Video created.")
            st.video(output)
            with open(output, "rb") as f:
                st.download_button("⬇️ Download MP4", f, file_name="ai_video.mp4", mime="video/mp4")

with tab2:
    photo = st.file_uploader("Upload a photo", type=["png","jpg","jpeg"])
    prompt = st.text_area("Motion prompt", placeholder="Slow camera push-in, natural movement...")
    if st.button("🖼️ Create Photo Video"):
        if not photo:
            st.error("Upload a photo first.")
        else:
            st.info("Photo-to-video requires a connected video model/API. The upload UI is ready; connect your chosen model in video/photo_to_video.py.")
