from app.models import Video, create_video, VideoStatus
from app.db import videos_db

ALLOWED_TRANSITIONS = {
    VideoStatus.CREATED: [VideoStatus.UPLOADING],
    VideoStatus.UPLOADING : [VideoStatus.PROCESSING],
    VideoStatus.PROCESSING: [VideoStatus.READY,VideoStatus.FAILED],
    VideoStatus.READY : [],
    VideoStatus.FAILED: []
}

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
    
    allowed_next_statuses = ALLOWED_TRANSITIONS.get(video.status,[])

    if status not in allowed_next_statuses:
        raise ValueError(f"Invalid transition from {video.status.value} to {status.value}")
    
    video.status = status

    return video


