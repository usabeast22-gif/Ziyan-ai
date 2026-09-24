import re

def split_script(script, target_minutes=1):
    text = re.sub(r"\s+", " ", script.strip())
    # Split on explicit scene markers first.
    parts = re.split(r"(?i)(?=scene\s*\d+\s*:)", text)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) == 1:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        parts = [s.strip() for s in sentences if s.strip()]
    return parts or [text]
