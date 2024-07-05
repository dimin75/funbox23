from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from datetime import datetime
# from redis import Redis
from redis import StrictRedis
import time
import json
import re
import uvicorn
import logging

log = logging.getLogger("uvicorn")

# app = FastAPI()
# redis_db = Redis()
redis_db = StrictRedis(host='localhost', port=6379, db=0)  # Подключение к Redis

def create_application() -> FastAPI:
    application = FastAPI()
    @application.get('/')
    def home():
        return {
            "message" : "tracking links api here..."
        }
    return application


app = create_application()

@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


class VisitedLink(BaseModel):
    links: list

class VisitedDomain(BaseModel):
    domain: str

def validate_link(link: str) -> bool:
    # Проверка валидности ссылки
    pattern = r'^(?:https?://)?([\w.-]+)'
    match = re.match(pattern, link)
    return bool(match)

@app.post("/visited_links")
def post_visited_links(visited_link: VisitedLink):
    current_time = int(datetime.now().timestamp())  # Получение текущего времени
    for link in visited_link.links:
        if validate_link(link):
            # Добавление ссылок и времени их посещения в Redis
            data = {'link': link, 'timestamp': current_time}
            redis_db.lpush('visited_links', json.dumps(data))
    return {"status": "ok"}

@app.get("/visited_domains")
def get_visited_domains(from_timestamp: int = 0, to_timestamp: int = int(time.time())):
    visited_domains = set()
    link_data_list = redis_db.lrange('visited_links', 0, -1)
    
    for link_data in link_data_list:
        link_data = link_data.decode()
        try:
            link = json.loads(link_data)
            timestamp = link.get('timestamp', 0)
            if from_timestamp <= timestamp <= to_timestamp:
                domain = link.get('link', '')
                if validate_link(domain):
                    match = re.match(r'^(?:https?://)?([\w.-]+)', domain)
                    domain = match.group(1)
                    visited_domains.add(domain)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to process link data")
    
    sorted_domains = sorted(visited_domains)
    return {"domains": sorted_domains, "status": "ok"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)