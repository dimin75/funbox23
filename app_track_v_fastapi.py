from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from redis import StrictRedis
import time, json
import ast, re
import logging
import uvicorn

log = logging.getLogger("uvicorn")


redis = StrictRedis(host='localhost', port=6379, db=0)  # Подключение к Redis

class VisitedLink(BaseModel):
    links: list

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

@app.post("/visited_links")
async def post_visited_links(visited_link: VisitedLink):
    current_time = int(datetime.now().timestamp())  # Получение текущего времени
    for link in visited_link.links:
        # Добавление ссылок и времени их посещения в Redis
        print('visited_links: ',{link: current_time})
        data = {'link': link, 'timestamp': current_time}
        redis.lpush('visited_links', json.dumps(data))
    return {"status": "ok"}

@app.get("/visited_domains")
async def get_visited_domains(request: Request):
    try:
        # Получение уникальных доменов, посещенных за заданный интервал времени
        from_timestamp = int(request.query_params.get('from', 0))
        to_timestamp = int(request.query_params.get('to', time.time()))
        # Извлекаем все записи из списка visited_links в бинарном формате
        visited_links = redis.lrange('visited_links', 0, -1)
        print('looking for data in range: ', from_timestamp, ' --> ', to_timestamp)

        # Фильтруем записи по временным интервалам на стороне приложения
        print('total records found in redis:', len(visited_links))
        domains = set()
        for x in range(len(visited_links)-1):
            cur_dat = ast.literal_eval(visited_links[x].decode(('utf-8')))
            timestamp = cur_dat['timestamp']
            if from_timestamp <= timestamp <= to_timestamp:
                pattern = r'^(?:https?://)?([\w.-]+)'
                domain = cur_dat['link']
                match = re.match(pattern, domain)
                if match:
                    domain2 = match.group(1)
                    domains.add(domain2)
                    print('domain found:',domain2)
        sorted_domains = sorted(domains)
        print({'domains': list(sorted_domains), 'status': 'ok'})
        result = {'domains': list(sorted_domains), 'status': 'ok'}
        json_str = json.dumps(result, ensure_ascii=False)
        return Response(content=json_str, media_type="application/json")        
    except Exception as e:
        return json.dump({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)