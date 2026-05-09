from fastapi import FastAPI,HTTPException
from app.models import Video,VideoCreateRequest,VideoStatusUpdateRequst,create_video,UploadUrlResponse
from app.db import videos_db
from app.services.video_service import create_video_service,update_video_status_service,get_video_service,generate_upload_url_service
from app.s3 import create_bucket_if_not_exists
app = FastAPI()

@app.on_event("startup")
def startup():
    create_bucket_if_not_exists()

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


@app.post(
    "/videos/{video_id}/upload-url",
    response_model=UploadUrlResponse
)
def generate_upload_url(video_id: str):
    try:
        response = generate_upload_url_service(video_id)
        if not response:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return response
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )