from fastapi import FastAPI,HTTPException
from app.models import Video,VideoCreateRequest,VideoStatusUpdateRequst,create_video
from app.db import videos_db
from app.services.video_service import create_video_service,update_video_status_service,get_video_service

app = FastAPI()

@app.get("/health")
def healthCheck():
    return {"status":"ok"}

@app.get("/ready")
def healthCheck():
    return {"status":"ready"}

@app.post("/videos/initiate-upload", response_model=Video)
def initiate_upload(request: VideoCreateRequest):
    return create_video_service(request.title,request.description)




@app.get("/videos/{video_id}",response_model=Video)
def get_video(video_id:str)->Video:
    video =  get_video_service(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video Not Found")
    
    return video

@app.patch("/videos/{video_id}/status",response_model=Video)
def update_video_status(video_id:str,request:VideoStatusUpdateRequst):
    try:
        video = update_video_status_service(video_id,request.status)
        if not video:
            raise HTTPException(status_code=404,detail="Video Not Found")
        
        video.status = request.status
        return video
    
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))


