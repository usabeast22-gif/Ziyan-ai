import os
import tempfile
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="My AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 My AI Video Generator")
st.write("Script → AI Video")

if "HF_TOKEN" not in st.secrets:
    st.error("HF_TOKEN Streamlit Secrets me add karo.")
    st.stop()

HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN,
)

st.subheader("📝 Script")

script = st.text_area(
    "Apni story/script likho:",
    height=220,
    placeholder="Example: Ek ladka subah apne shehar ki sadak par chal raha hai..."
)

duration = st.slider(
    "Video duration (per generated clip)",
    min_value=2,
    max_value=10,
    value=4
)

style = st.selectbox(
    "Video style",
    [
        "Cinematic realistic",
        "3D animation",
        "Anime",
        "Cartoon"
    ]
)

if st.button("🚀 Generate AI Video", use_container_width=True):

    if not script.strip():
        st.warning("Pehle script likho.")
        st.stop()

    prompt = f"""
Create a {style} video based on this story:

{script}

Show the main character clearly.
Natural human movement.
Cinematic camera movement.
Consistent character appearance.
Detailed environment.
High quality.
"""

    st.info("AI video generate ho raha hai... thoda time lagega.")

    try:
        video_bytes = client.text_to_video(
            prompt,
            model="Wan-AI/Wan2.1-T2V-1.3B",
            num_frames=int(duration * 16),
        )

        output_path = os.path.join(
            tempfile.gettempdir(),
            "ai_generated_video.mp4"
        )

        with open(output_path, "wb") as f:
            f.write(video_bytes)

        st.success("✅ Video ready!")

        st.video(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                "⬇️ Download Video",
                f,
                file_name="my_ai_video.mp4",
                mime="video/mp4"
            )

    except Exception as e:
        st.error("Video generation failed.")
        st.code(str(e))
        st.info(
            "Check karo ki HF token me Inference Providers permission hai "
            "aur account me provider inference available hai."
        )
