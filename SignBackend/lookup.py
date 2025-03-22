from fastapi import FastAPI, HTTPException
import json
import os
import requests
from pose_format import Pose
from fastapi.responses import FileResponse
import tempfile
from pose_format.pose_visualizer import PoseVisualizer
from concatenate import concatenate_poses


app = FastAPI()

# Set the path where your JSON index files are stored
INDEX_DIR = "Indexes"

# Function to load JSON data
def load_json(file_path):
    if not os.path.exists(file_path):
        return {}  # Return empty dict if file doesn't exist

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return {}  # Return empty dict if JSON is invalid
    
def fetch_and_load_poses(urls):
    pose_objects = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for errors

            data_buffer = response.content  # Read binary content
            pose = Pose.read(data_buffer)  # Load into Pose object
            pose_objects.append(pose)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    return pose_objects
async def generate_video_from_poses(pose_objects):
    """Concatenates Pose objects, saves .pose, and converts to .mp4"""

    # Step 1: Concatenate Pose Files
    final_pose = concatenate_poses(pose_objects)

    # Step 2: Save final_pose to a temporary file
    temp_dir = tempfile.gettempdir()
    pose_path = os.path.join(temp_dir, "final_output.pose")
    with open(pose_path, "wb") as f:
        final_pose.write(f)

    # Step 3: Load Pose and Convert to Video
    with open(pose_path, "rb") as f:
        pose = Pose.read(f.read())

    visualizer = PoseVisualizer(pose)

    # Step 4: Save video
    video_path = os.path.join(temp_dir, "final_output.mp4")
    visualizer.save_video(video_path, visualizer.draw())

    return video_path




@app.post("/lookup")
async def lookup(words: list[str]):
    result_links = []
    pose_objects = []
    for word in words:
        if not word:
            continue  # Skip empty words

        first_letter = word[0].upper()  # Get the first letter
        print(first_letter)
        json_file = os.path.join(INDEX_DIR, f"pose_files_urls_{first_letter}.json")

        data = load_json(json_file)  # Load corresponding JSON file
        
        # Find the URL for the word if available
        url = data.get(f"{word.lower()}.pose")  # Assuming keys are stored in lowercase
        print(url)
        if url:
            result_links.append(url)

    if not result_links:
        raise HTTPException(status_code=404, detail="No links found for given words")
    pose_objects=fetch_and_load_poses(result_links)
    if not pose_objects:
        raise HTTPException(status_code=404, detail="Error in fetch_and_load_poses")
    video_path=await generate_video_from_poses(pose_objects)
    return FileResponse(video_path, media_type="video/mp4", filename="sign_language_video.mp4")
    

