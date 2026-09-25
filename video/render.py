
import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

def _ffmpeg():
    return imageio_ffmpeg.get_ffmpeg_exe()

def _font(size=42):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def _make_card(text, path):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), "black")
    draw = ImageDraw.Draw(img)
    font = _font(42)

    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= W - 140:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    line_h = 58
    y = (H - len(lines) * line_h) // 2
    for ln in lines:
        box = draw.textbbox((0, 0), ln, font=font)
        x = (W - (box[2] - box[0])) // 2
        draw.text((x, y), ln, fill="white", font=font)
        y += line_h
    img.save(path)

def make_video(scenes, target_minutes, fps=24):
    ff = _ffmpeg()
    out_dir = tempfile.mkdtemp(prefix="ai_video_")
    out = os.path.join(out_dir, "ai_video.mp4")
    per_scene = max(3.0, (target_minutes * 60) / max(1, len(scenes)))
    clips = []

    for i, text in enumerate(scenes):
        card = os.path.join(out_dir, f"scene_{i}.png")
        clip = os.path.join(out_dir, f"clip_{i}.mp4")
        _make_card(text, card)
        subprocess.run([
            ff, "-y", "-loop", "1", "-i", card,
            "-t", str(per_scene), "-r", str(fps),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-vf", "scale=1280:720", clip
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        clips.append(clip)

    concat = os.path.join(out_dir, "concat.txt")
    with open(concat, "w", encoding="utf-8") as f:
        for c in clips:
            f.write("file '" + c.replace("'", "'\\''") + "'\n")

    subprocess.run([
        ff, "-y", "-f", "concat", "-safe", "0",
        "-i", concat, "-c", "copy", out
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return out
