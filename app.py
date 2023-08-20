import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import cv2
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from main import management,check,gen_frames,updatedValues,get_list_data
import json
load_dotenv('.env')
dc = {"1":["recording.mp4","CMR_bike.mp4"],"2":["gvp11.mp4","gvp2.mp4"]}
app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get('/companies')
def companies():
    data = [{"id":1,"name":"CMR CENTRAL","levels":2,"slots":[0]*2},{"id":2,"name":"GVP","levels":2,"slots":[0]*2},{"id":3,"name":"PALM BEACH","levels":2,"slots":[0]*2},{"id":4,"name":"SPENCERS","levels":1,"slots":[0]*1}]
    return JSONResponse(content=data)



@app.get('/gvp1video')
def gvp1video():
    return StreamingResponse(management("gvp11.mp4","gvppickle1",10), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/gvp2video')
def gvp2video():
    return StreamingResponse(management("gvp2.mp4","gvppickle2",10), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/cmr1video')
def cmr1video():
    return StreamingResponse(management("CMR_bike.mp4","bikepicklefinal2",4), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/cmr2video')
def cmr2video():
    return StreamingResponse(management("recording.mp4","carpicklefinal",10), media_type='multipart/x-mixed-replace; boundary=frame')
@app.post('/slots/')
def slots(i,l:int):
    global dc
    data = {"slots":updatedValues(dc[i][l-1]),"slotname":get_list_data(dc[i][l-1])}
    return JSONResponse(content=data)

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)