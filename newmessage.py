#!/usr/bin/python3
import sys
import praw
import time
import requests
import json
import textwrap

CONFIG_FILE='config.json'

def shortened_text(text):
    return textwrap.shorten(text, config['max_text_length'], placeholder='..')

def handle_comment(comment):
    send = (comment.author.name,
            shortened_text(comment.submission.title),
            shortened_text(comment.body),
            'https://reddit.com' + comment.context)
    notify(*send)

def handle_message(message):
    send = (message.author.name,
            message.subject,
            shortened_text(message.body),
            'https://www.reddit.com/message/inbox/#thing_{}'.format(message.fullname))
    notify(*send)

def notify(author, subject, text, url):
    if first and config['ignore_old_unread']:
        return
    if config['discord']['enabled']:
        notify_discord(author, subject, text, url)
    if config['slack']['enabled']:
        notify_slack(author, subject, text, url)
    if config['telegram']['enabled']:
        notify_telegram(author, subject, text, url)
    if config['debug']:
        print('{}: [{}] {} {}'.format(author, subject, text, url))

def notify_discord(author, subject, text, url):
    message = '*{}:* [{}] {} {}'.format(author, subject, text, url)
    payload = { 'content': message }
    headers = { 'Content-Type': 'application/json', }
    requests.post(config['discord']['webhook'], data=json.dumps(payload), headers=headers)

def notify_slack(author, subject, text, url):
    message = '*{}:* [{}] {} {}'.format(header, body, url)
    payload = { 'text': message }
    headers = { 'Content-Type': 'application/json', }
    requests.post(config['slack']['webhook'], data=json.dumps(payload), headers=headers)

def notify_telegram(author, subject, text, url):
    message = '<b>{}:</b> [{}] {} {}'.format(author, subject, text, url)
    payload = { 
        'chat_id': config['telegram']['chat_id'],
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post("https://api.telegram.org/bot{}/sendMessage".format(config['telegram']['token']),
                  data=payload)

with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

r = praw.Reddit(
    user_agent = config['reddit']['user_agent'],
    client_id = config['reddit']['client_id'],
    client_secret = config['reddit']['client_secret'],
    username = config['reddit']['username'],
    password = config['reddit']['password']
)

first = True
inbox_stream = r.inbox.stream(pause_after=-1)    

while True:
    try:
        for item in inbox_stream:
            if item is None:
                break
            if isinstance(item, praw.models.Comment):
                handle_comment(item)
            if isinstance(item, praw.models.Message):
                handle_message(item)

        first = False
        time.sleep(5)
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
    except Exception as e:
        print('Error:', e)
        time.sleep(5)
