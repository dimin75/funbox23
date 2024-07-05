from flask import Flask, request, jsonify
import redis, json
import time
import ast, re

app = Flask(__name__)

# Подключение базы REDIS
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# обработка POST-запросов, проходящих через сервер.
@app.route('/visited_links', methods=['POST'])
def visited_links():
    try:
        links = request.json.get('links', [])
        if not isinstance(links, list):
            return jsonify({'status': 'error', 'message': 'Invalid format for links'}), 400
        timestamp = int(time.time())
        for link in links:
            print('visited_links: ',{link: timestamp})
            data = {'link': link, 'timestamp': timestamp}
            redis_db.lpush('visited_links', json.dumps(data))
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    try:
        from_timestamp = int(request.args.get('from', 0))
        to_timestamp = int(request.args.get('to', time.time()))

        # Извлекаем все записи из списка visited_links в бинарном формате
        domain_jsons = redis_db.lrange('visited_links', 0, -1)

        # Фильтруем записи по временным интервалам на стороне приложения
        domains = set()
        for x in domain_jsons:
            cur_dat = ast.literal_eval(x.decode(('utf-8')))
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
        return json.dumps(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)