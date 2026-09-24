# My AI Video Generator

## What is included
- Streamlit web interface
- Script input and scene splitting
- 1–20 minute target duration
- Local MP4 rendering through FFmpeg
- Photo-to-video adapter ready for a real model

## Important
The included renderer creates a reliable script-based video. It is **not** a fake claim of AI text-to-video generation. Real AI visuals, character voices and lip-sync require a connected model/service and compute.

## Run locally
1. Install FFmpeg.
2. Install Python dependencies:
   `pip install -r requirements.txt`
3. Start:
   `streamlit run app.py`

## Next integration points
- `video/render.py`: replace scene-card rendering with a text-to-video model.
- `video/photo_to_video.py`: connect an image-to-video model.
- Add a TTS adapter for character speech.
- Add a lip-sync adapter.
