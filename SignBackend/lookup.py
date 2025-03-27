from fastapi import FastAPI, HTTPException
import json
import os
import requests
from pose_format import Pose
from fastapi.responses import FileResponse
import tempfile
from pose_format.pose_visualizer import PoseVisualizer
from concatenate import concatenate_poses
from generate_dynamic_video import get_pose_file, search_shortest_youtube_pose, download_video, convert_video_to_pose, upload_to_cloudinary, update_json_index

app = FastAPI()

# Set the path where your JSON index files are stored
INDEX_DIR = "Indexes"

def load_json(file_path):
    if not os.path.exists(file_path):
        return {}  # Return empty dict if file doesn't exist
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return {}

def fetch_and_load_poses(urls):
    pose_objects = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data_buffer = response.content
            pose = Pose.read(data_buffer)
            pose_objects.append(pose)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return pose_objects

async def generate_video_from_poses(pose_objects):
    final_pose = concatenate_poses(pose_objects)
    temp_dir = tempfile.gettempdir()
    pose_path = os.path.join(temp_dir, "final_output.pose")
    with open(pose_path, "wb") as f:
        final_pose.write(f)
    
    with open(pose_path, "rb") as f:
        pose = Pose.read(f.read())
    visualizer = PoseVisualizer(pose)
    video_path = os.path.join(temp_dir, "final_output.mp4")
    visualizer.save_video(video_path, visualizer.draw())
    return video_path

@app.post("/lookup")
async def lookup(words: list[str]):
    result_links = []
    pose_objects = []
    for word in words:
        if not word:
            continue

        first_letter = word[0].upper()
        json_file = os.path.join(INDEX_DIR, f"pose_files_urls_{first_letter}.json")
        data = load_json(json_file)
        url = data.get(f"{word.lower()}.pose")
        
        if url:
            result_links.append(url)
        else:
            print(f"{word} not found in index. Generating dynamically...")
            generated_url = get_pose_file(word)
            if generated_url and "http" in generated_url:
                result_links.append(generated_url)

    if not result_links:
        raise HTTPException(status_code=404, detail="No links found for given words")
    
    pose_objects = fetch_and_load_poses(result_links)
    if not pose_objects:
        raise HTTPException(status_code=404, detail="Error in fetch_and_load_poses")
    
    video_path = await generate_video_from_poses(pose_objects)
    return FileResponse(video_path, media_type="video/mp4", filename="sign_language_video.mp4")
