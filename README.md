# Unread Reddit inbox message alert

_Based on [NewPost](https://github.com/bag-man/NewPost) by Owen Garland._

This script will monitor your reddit inbox, and send push notifications to an IM platform of your choice. Currently, Slack, Discord, and Telegram are supported.

PLEASE NOTE: At the moment this will only notify on new reddit messages, **not** new chats. I hope to add support for chats once reddit adds them to its API specs, but for now chats are still an experimental feature.

You just need praw, so run:

    pip install -r requirements.txt

To install the dependencies. You then need to configure copy the `config.json.template` file to `config.json` and update it with the api keys and settings you want. 

### Reddit 
Log into your account and go to: https://www.reddit.com/prefs/apps/. Click "create another app", pick a name and description, and set the redirect url to something like `http://localhost:8080`.

The identifier below your app name should be filled into _client\_id_ in `config.json`. The secret is your _client\_secret_ and you can pick an arbitrary _user\_agent_. Finally, fill in your account username and password.

### Slack
Create a slack app and get a webhook for the channel you would like to post to: https://api.slack.com/incoming-webhooks#getting-started. 

### Discord
In your server settings create a webhook: https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks

### Telegram
In Telegram, message `/newbot` to @BotFather. Follow the steps and you will receive a token at the end, copy this token to your `config.json`.

To get the chat ID, send your bot a message and open https://api.telegram.org/bot[TOKEN]/getUpdates in your browser, you will find an ID there.
