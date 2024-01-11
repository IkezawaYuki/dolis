import azure.functions as func
import logging
import os
import json
import requests



azure_app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
    


@azure_app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        slack_event = req_body.get('event')
        if slack_event.get("type") == "app_mention":
            user_id = slack_event.get("user")
            channel_id = slack_event.get("channel")
            send_slack_message(channel_id, f"<@{user_id}>さん、ファイヤー!!!!")
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

