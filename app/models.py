from enum import Enum
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

class VideoStatus(str,Enum):
    CREATED="CREATED"
    PROCESSING="PROCESSING"
    UPLOADING="UPLOADING"
    READY="READY"
    FAILED="FAILED"


class Video(BaseModel):
    id:str
    title:str
    description:str | None = None
    createdAt : datetime
    status: VideoStatus

class VideoCreateRequest(BaseModel):
    title: str
    description : str | None = None

class VideoStatusUpdateRequst(BaseModel):
    status: VideoStatus

class UploadUrlResponse(BaseModel):
    video_id : str
    upload_url: str
    

def create_video(title: str, description: str | None = None) -> Video: 
    return Video(
        id=str(uuid4()),
        title=title,
        description=description,
        createdAt=datetime.utcnow(),
        status=VideoStatus.CREATED
    )

