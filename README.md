# Anonymous Slack Messenger Bot

## Install
```{bash}
python3 -m pip install -r requirements.txt
```
1. Create [new plugin on Slack](https://api.slack.com/)
2. Create .env file in the base directory with the following:
```{bash}
SLACK_TOKEN=<token from slack API>
SIGNING_SECRET=<signing secret from slack API>
SLACK_HEADER="New Suggestion!\n"
SLACK_RECIPIENT=<recipient slack name, can be found by querying all users>
SLACK_MEMBER_ID=<Alternative Member ID instead of recipient name>
FLASK_PORT=<open port>
FLASK_DEBUG=<debug setting>
```
3. Spin up [NGrok server](https://ngrok.com/) (for local testing)
4. Add NGrok URL into Slack API events controller
5. Add Slash command into Slack Bot
6. Setup Slash command URL as: `<NGrokURL>/slack/events/`
7. Give bot permission pertaining to channel reads, message writes, and user listing (including ephemeral messages, direct messages, and channel messages)
8. Add bot into Slack testing workspace

## Usage
From within any channel you can use the `/suggest <suggestion text>` command.