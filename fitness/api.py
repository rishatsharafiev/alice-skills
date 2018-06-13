# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    data = {}
    with open('data.json') as file:
        data = json.load(file)
    user_id = req['session']['user_id']
    original_utterance = req.get('request', {'original_utterance': ''})['original_utterance']
    original_utterance = original_utterance.lower().strip().strip(',').strip('.')

    messages = data.get('messages', {})
    questions = data.get('questions', [])
    suggests = get_suggests(
        data.get('suggests', '')
    )

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': suggests
        }

        res['response']['text'] = messages.get('hello', '')
        res['response']['buttons'] = suggests
        return

    for question in questions:
        input_text = question.get('input', '')
        if original_utterance == input_text:
            output_text = question.get('output', '')
            suggests = get_suggests(
                question.get('suggests', '')
            )

            res['response']['text'] = output_text
            res['response']['buttons'] = suggests

            sessionStorage[user_id] = {
                'suggests': suggests
            }
            break
    else:
        res['response']['text'] = messages.get('default', '')
        res['response']['buttons'] = suggests

        sessionStorage[user_id] = {
            'suggests': suggests
        }

def get_suggests(suggests):
    new_suggests = []
    for suggest in suggests:
        new_suggest = {'hide': True}

        if 'title' in suggest:
            new_suggest['title'] = suggest['title']
            if 'url' in suggest:
                new_suggest['url'] = suggest['url']
            new_suggests.append(new_suggest)

    return new_suggests
