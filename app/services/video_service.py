from app.models import Video, create_video, VideoStatus
from app.db import videos_db

def create_video_service(title: str,description: str | None = None) -> Video:
    video = create_video(title,description)
    videos_db[video.id] = video
    return video

def get_video_service(video_id: str) -> Video | None:
    return videos_db.get(video_id)

def update_video_status_service(video_id : str, status: VideoStatus) -> Video | None:
    video = videos_db.get(video_id)

    if not video:
        return None
    
    video.status = status

    return video


