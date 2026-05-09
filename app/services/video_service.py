from app.models import Video, create_video, VideoStatus,UploadUrlResponse
from app.db import videos_db
from app.s3 import s3_client,BUCKET_NAME

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


def generate_upload_url_service(video_id:str)->UploadUrlResponse | None:
    video = videos_db.get(video_id)

    if not video:
        return None

    if video.status != VideoStatus.CREATED:
        raise ValueError(f"Upload URL can only be generated when status of video is CREATED")
    
    video.status = VideoStatus.UPLOADING

    # fake preassigned URL 
    # upload_url = f"https://aws.com.s3/uploads/{video.id}"

    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket":BUCKET_NAME,
            "Key":f"raw-videos/{video.id}.mp4"
        },
        ExpiresIn=3600
    )

    return UploadUrlResponse(video_id=video_id,upload_url=upload_url)


