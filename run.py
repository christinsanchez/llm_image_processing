import os
from data_pipeline_christin import download_video, extract_frames, create_photo_grids, save_images_as_base64
from prompt_llm_christin import submit_base64_images_for_description, initialize_openai_client

# Define paths
video_url = "https://www.youtube.com/watch?v=pnY87IcRKuY"
video_path = "./youtube_vid"
video_file = os.path.join(video_path, "nursingvideo.mp4")
frame_dir = "./frames"
grid_output_dir = "./5x5_300"
base64_output_dir = "./5x5_300"

# Step 1: Download video
download_video(video_path, video_url)

# Step 2: Extract frames from video
extract_frames(video_file, frame_dir, step_size=25)

# Step 3: Create photo grids
create_photo_grids(frame_dir, grid_output_dir, window_size=300, n=5, grid=True)

# Step 4: Convert images to base64
save_images_as_base64(grid_output_dir, base64_output_dir)

# Step 5: Submit base64 images for LLM processing
client = initialize_openai_client()
submit_base64_images_for_description(base64_output_dir, client, "./different_prompts/behavior_interaction.txt")
