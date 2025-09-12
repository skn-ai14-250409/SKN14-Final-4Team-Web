# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key="OPENAI_API_KEY")


# ── CORS: 개발 중엔 * 허용, 배포 시 Django 도메인만 허용하세요 ──
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ex) ["https://loop-label.ap-northeast-2.elasticbeanstalk.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LookItem(BaseModel):
    id: int
    image: str
    look_name: str
    look_desc: str

class ChatIn(BaseModel):
    # 프론트가 "message"로 보내게 할 것. (혹은 "msg"도 허용하고 싶다면 alias 사용)
    message: str = Field(..., alias="msg")

class ChatOut(BaseModel):
    type: str = "ai"
    msg1: str
    msg2: Optional[str] = None
    list: List[LookItem] = []
    voice: Optional[str] = None
    time: Optional[str] = None

def _cur_time():
    return datetime.now().strftime("%I:%M %p")  # "09:27 AM" 형태

@app.post("/chat", response_model=ChatOut)
async def chat(req: ChatIn):
    user_text = req.message.strip()

    rsp = client.chat.completions.create(
        model="ft:gpt-4.1-mini-2025-04-14:skn14:hjk-0911-v01:CEUOn4Sy",
        messages=[{"role": "user", "content": user_text}],
        temperature=0.7,
        top_p=0.9,
    )
    answer = rsp.choices[0].message.content
    
    
    demo_list = [
        LookItem(id=9,  image="/static/images/dummy/dummy_look_1.jpg", look_name="스마트 캐주얼",   look_desc="💼 클래식하고 단정한 재활용울 수트룩"),
        LookItem(id=11, image="/static/images/dummy/dummy_look_2.jpg", look_name="미니멀 테일러드", look_desc="✨ 가볍고 활동성 높은 리사이클 셋업룩"),
    ]
    return ChatOut(
        msg1=answer, 
        list=[],
        voice=None, # tts 나중에 추가
        time=_cur_time()
    )
