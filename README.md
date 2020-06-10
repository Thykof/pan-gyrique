# Panégyrique

This is a slack bot that allow users to send anonymous compliment and congratulation.

## Tech

This is a web server coded in python with the Flask framework.

## Develop

Run:

    export export SLACK_SIGNING_SECRET=000000000000000
    export export SLACK_BOT_TOKEN=000000000000000

Launch: `python3 main.py`.

Start ngrock: `./ngrok http 3000`.

## Production

The app is deployed in heroku at https://panegyrique.herokuapp.com.

The two variables `SLACK_SIGNING_SECRET` and `SLACK_BOT_TOKEN` are defined in the heroku dashboard as Config Vars.

It uses `gunicorn`.
