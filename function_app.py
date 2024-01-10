import azure.functions as func
import logging
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


azure_app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@azure_app.route(route="http_trigger", auth_level=func.AuthLevel.FUNCTION)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"ハロー, {name}.")
    else:
        return func.HttpResponse(
             "うまくいってるぜ！",
             status_code=200
        )