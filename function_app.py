import azure.functions as func
import logging
import os
import json
import requests
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
azure_app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
    

@azure_app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        slack_event = req_body.get('event')
        if slack_event.get("type") == "app_mention":
            print(slack_event)
            user_id = slack_event.get("user")
            channel_id = slack_event.get("channel")
            message = slack_event.get("text")
            resp = send_gpt(message)
            send_slack_message(channel_id, f"<@{user_id}>{resp}")
    except ValueError as e:
        print(e)
    return func.HttpResponse("ファイヤー!", status_code=200)


def send_slack_message(channel_id, message):
    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_BOT_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel_id,
        "text": message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        logging.error(f"Slack APIへのリクエストに失敗しました。ステータスコード: {response.status_code}")


def send_gpt(message):
    chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{message}",
                }
            ],
            model="gpt-4",
        )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content