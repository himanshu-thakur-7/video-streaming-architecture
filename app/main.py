from fastapi import FastAPI,HTTPException
from app.models import Video,VideoCreateRequest,VideoStatusUpdateRequst,create_video
from app.db import videos_db

app = FastAPI()

@app.get("/health")
def healthCheck():
    return {"status":"ok"}

@app.get("/ready")
def healthCheck():
    return {"status":"ready"}

@app.post("/videos/initiate-upload", response_model=Video)
def initiate_upload(request: VideoCreateRequest):
    video = create_video(
        title=request.title,
        description=request.description
    )
    videos_db[video.id] = video

    print(f"videos db: {videos_db}")
    return video



@app.get("/videos/{video_id}",response_model=Video)
def get_video(video_id:str)->Video:
    print(f"videos db: {videos_db}")
    video = videos_db.get(video_id)

    if not video:
        raise HTTPException(status_code=404,detail="Video Not Found")

    return video

@app.patch("/videos/{video_id}/status",response_model=Video)
def update_video_status(video_id:str,request:VideoStatusUpdateRequst):
    video = videos_db.get(video_id)
    if not video:
        raise HTTPException(status_code=404,detail="Video Not Found")
    
    video.status = request.status
    return video