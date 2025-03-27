import os
import re
import subprocess
import requests
import json
import cloudinary
import cloudinary.uploader
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def parse_duration(duration_str):
    match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    minutes = int(match.group(1)) if match.group(1) else 0
    seconds = int(match.group(2)) if match.group(2) else 0
    return minutes * 60 + seconds

def search_shortest_youtube_pose(word):
    query = f"{word} Indian Sign Language"
    search_request = youtube.search().list(q=query, part="id,snippet", type="video", maxResults=5)
    search_response = search_request.execute()
    
    if not search_response.get("items"):
        return None  
    
    video_ids = [item["id"]["videoId"] for item in search_response["items"]]
    details_request = youtube.videos().list(part="contentDetails", id=",".join(video_ids))
    details_response = details_request.execute()
    
    min_duration = float("inf")
    shortest_video = None
    
    for item in details_response["items"]:
        video_id = item["id"]
        duration = parse_duration(item["contentDetails"]["duration"])
        if duration < min_duration:
            min_duration = duration
            shortest_video = f"https://www.youtube.com/watch?v={video_id}"
    
    return shortest_video

def delete_local_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ Deleted file: {file_path}")

def download_video(video_url, output_filename):
    command = ["yt-dlp", "-f", "best[ext=mp4]", "-o", output_filename, video_url]
    subprocess.run(command, check=True)
    return output_filename

def convert_video_to_pose(video_filename, pose_filename):
    command = ["video_to_pose", "--format", "mediapipe", "-i", video_filename, "-o", pose_filename]
    try:
        subprocess.run(command, check=True)
        return pose_filename
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in pose conversion: {e}")
        return None

def upload_to_cloudinary(pose_filename, word):
    response = cloudinary.uploader.upload_large(
        pose_filename,
        resource_type="raw",
        folder="pose_files/",
        public_id=f"pose_files/{word}"
    )
    return response.get("secure_url")

def update_json_index(word, cloudinary_url):
    json_folder = "Indexes"
    first_letter = word[0].upper()
    json_file_path = os.path.join(json_folder, f"pose_files_urls_{first_letter}.json")
    
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    
    key = f"{word}.pose"
    data[key] = cloudinary_url
    
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    print(f"✅ Updated JSON index: {json_file_path}")

def get_pose_file(word):
    json_folder = "Indexes"
    key = f"{word}.pose"
    
    for file in os.listdir(json_folder):
        if file.endswith(".json"):
            file_path = os.path.join(json_folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if key in data:
                    return data[key]
    
    youtube_url = search_shortest_youtube_pose(word)
    if youtube_url:
        video_filename = f"{word}.mp4"
        download_video(youtube_url, video_filename)
        pose_filename = f"{word}.pose"
        converted_pose = convert_video_to_pose(video_filename, pose_filename)
        
        if converted_pose:
            cloudinary_url = upload_to_cloudinary(pose_filename, word)
            update_json_index(word, cloudinary_url)
            
            # Delete local files after processing
            delete_local_file(video_filename)
            delete_local_file(pose_filename)
            
            return cloudinary_url
    
    return None
