# llm_image_processing

# README

## Project Overview
This project consists of two Python scripts for processing video frames and generating LLM-based descriptions.

### 1. `data_pipeline_christin.py`
This script performs the following tasks:
- Downloads a YouTube video.
- Extracts frames from the video.
- Creates photo grids from extracted frames.
- Converts images to base64 format and saves them.
- Resizes and preprocesses images for storage.

### 2. `prompt_llm_christin.py`
This script uses OpenAI's API to:
- Load base64-encoded images.
- Generate descriptions for nursing training video frames using LLM.
- Save the generated descriptions in a structured JSON format.

---

## Installation & Setup

### Prerequisites
Make sure you have the following dependencies installed:
```bash
pip install opencv-python-headless pillow pytube pytubefix openai numpy
```

### API Key Setup
The `prompt_llm_christin.py` script requires an OpenAI API key. Replace the existing placeholder key in the script with your valid API key.

---

## How to Run

To execute the scripts, use the provided `run.sh` script.

```bash
bash run.sh
```

Alternatively, you can manually run them:

```bash
python data_pipeline_christin.py
python prompt_llm_christin.py
```

---

## Output Files
- Extracted frames are stored in `./frames`.
- Photo grids are saved in `./5x5_300`.
- Base64-encoded image text files are stored in `./5x5_300`.
- LLM-generated descriptions are saved in `./different_prompts/behavior_interaction.txt`.

---

## Notes
- Ensure you have sufficient storage space for the extracted frames and grids.
- Adjust `step_size` in `extract_frames()` to control frame extraction frequency.
- Modify the LLM prompt in `prompt_llm_christin.py` for different description styles.

