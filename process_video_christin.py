from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
import os
import requests

from pytubefix import YouTube
from pytubefix.cli import on_progress


# # where to save 
# SAVE_PATH = "/youtube_vid" 

# # link of the video to be downloaded 
# link = "https://www.youtube.com/watch?v=gUWJ-6nL5-8"

# try: 
#     # object creation using YouTube 
#     yt = YouTube(link) 
# except: 
#     #to handle exception 
#     print("Connection Error") 

# # Get all streams and filter for mp4 files
# mp4_streams = yt.streams.filter(file_extension='mp4').all()

# # get the video with the highest resolution
# d_video = mp4_streams[-1]

# try: 
#     # downloading the video 
#     d_video.download(output_path=SAVE_PATH)
#     print('Video downloaded successfully!')
# except: 
#     print("Some Error!")


client = OpenAI(api_key = dev_key)

video = cv2.VideoCapture("youtube_vid/nursing_training_christin.mp4")

base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read.")

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames from a video that I want to upload. Generate a compelling description that I can upload along with the video.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)