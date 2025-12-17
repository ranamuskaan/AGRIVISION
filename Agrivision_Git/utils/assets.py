# utils/assets.py
import base64
import os

def get_base64_of_bin_file(bin_file: str):
    if not os.path.exists(bin_file):
        return None
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_video_base64(video_file: str):
    if not os.path.exists(video_file):
        return None
    with open(video_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()