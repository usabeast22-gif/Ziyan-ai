import os, shutil, subprocess, tempfile

def _ffmpeg():
    return shutil.which("ffmpeg")

def make_video(scenes, target_minutes, fps=24):
    ff = _ffmpeg()
    if not ff:
        raise RuntimeError("FFmpeg is not installed on this machine.")

    out_dir = tempfile.mkdtemp(prefix="ai_video_")
    out = os.path.join(out_dir, "ai_video.mp4")

    # A reliable local renderer: creates a clean scene-card video from the script.
    # Replace this renderer with a text-to-video model in production.
    per_scene = max(3, (target_minutes * 60) / max(1, len(scenes)))
    clips=[]
    for i, text in enumerate(scenes):
        txt=os.path.join(out_dir, f"scene_{i}.txt")
        with open(txt,"w",encoding="utf-8") as f:
            f.write(text.replace(":", r"\:").replace("'", r"\'"))
        clip=os.path.join(out_dir, f"clip_{i}.mp4")
        cmd=[
            ff,"-y","-f","lavfi","-i",
            f"color=c=black:s=1280x720:r={fps}",
            "-t",str(per_scene),
            "-vf",
            f"drawtext=fontcolor=white:fontsize=42:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
            f"textfile='{txt}':x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=12",
            "-c:v","libx264","-pix_fmt","yuv420p",clip
        ]
        subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        clips.append(clip)

    concat=os.path.join(out_dir,"concat.txt")
    with open(concat,"w",encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    subprocess.run([ff,"-y","-f","concat","-safe","0","-i",concat,"-c","copy",out],
                   check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return out
