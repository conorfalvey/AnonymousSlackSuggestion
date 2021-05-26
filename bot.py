#!/usr/bin/env python3
######################
# Author: Conor Falvey
# Version: 0.1.0
# Email: conor.falvey22@gmail.com
# Status: Dev
######################
# Base packages
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Server/API packages
from flask.wrappers import Response
from flask import Flask, request, Response
import slack
from slackeventsapi import SlackEventAdapter

# Load environment variables and verify
env_path = Path(".") / ".env"
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

required_keys = [
    "SIGNING_SECRET",
    "SLACK_TOKEN",
    "SLACK_HEADER",
    "FLASK_DEBUG",
    "FLASK_PORT",
]
either_keys = ["SLACK_MEMBER_ID", "SLACK_RECIPIENT"]

if not all([key in os.environ for key in required_keys]) or not any(
    [key in os.environ for key in either_keys]
):
    raise EnvironmentError("Not all required environment variables are set!")

# Server configs and API secrets
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"], "/slack/events", app
)

slackClient = slack.WebClient(token=os.environ["SLACK_TOKEN"])
BOT_ID = slackClient.api_call("auth.test")["user_id"]


@app.route("/matt", methods=["POST"])
def anonSuggest():
    """ Recieve POST requests from Slack API
    served by the `/suggest` command."""
    data = request.form
    text = data.get("text")

    # retrieve_recipient looks up with user_id from the provided
    # recipient username in the .env file. It queries all members
    # and matches on the username if the member ID is not given.
    if not os.environ["SLACK_MEMBER_ID"]:
        os.environ["SLACK_MEMBER_ID"] = retrieve_recipient()

    if not os.environ["SLACK_MEMBER_ID"]:
        return Response(), 500

    # send_suggestion appends a message prefix defined in the
    # .env file. They're just concatenated.
    send_suggestion(slackClient, recipient=os.environ["SLACK_MEMBER_ID"], text=text)
    return Response(), 200


def retrieve_recipient():
    for rec in slackClient.users_list()["members"]:
        if rec["name"] == os.environ["SLACK_RECIPIENT"]:
            return rec["id"]
    return None


def send_suggestion(slackClient, recipient, text):
    updated_text = os.environ["SLACK_HEADER"] + text
    # Channel arg can be a community channel or a single user ID.
    slackClient.chat_postMessage(channel=recipient, text=updated_text)


# Server ran from additional asyncio block in order to run multiple servers
# from a single bot file. I.e. We could add a block for a server running
# a discord client directly here and have them run concurrently.
async def run_slack():
    app.run(debug=os.environ["FLASK_DEBUG"], port=os.environ["FLASK_PORT"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_slack())
    loop.run_forever()
