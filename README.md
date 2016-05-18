
A Slack bot used for voting committee members in the [Slack team](https://pythonnigeria.slack.com) of the [Nigeria Python Users Group](https://wiki.python.org/moin/LocalUserGroups#Nigeria).

To run:

Install dependencies with:

```bash
$ pip install -r requirements.txt
```

Go to your Slack team.
Create a Slack bot and retrieve your bot token.
For the bot's general operations, you should use the bot's token.

If you need to do more restricted things like "message deletion", and depending on your Slack team's settings, you can additionally provide the test token of an admin's account if they agree to share this with you.

Store the following environment variables:

```bash
$ export VOTEBOT_TOKEN='your_slack_bot_token'
#'your_slack_bot_token' looks like this:
#xoxb-44000072424-MITpf7zISPGGwoOJf6heio3r

$ export VOTEBOT_ADMIN_TOKEN='your_slack_account_test_token'
#Get your account test token here:
#https://api.slack.com/docs/oauth-test-tokens
#'your_slack_account_test_token' looks like this:
#xoxp-8212479232-8832743651-22913437991-4f0b7cbe1a

$ export VOTEBOT_CONFIG_MODE='your_config_mode'
# 'your_config_mode' should be one of: dev, deploy, test
```

Run bot with:

```bash
$ python run.py
```

*Working commands:*

    List of commands:
       :about, :admins, :clear, :ctrl, :help, :initiate

    For help on a command, type:
       :help [command]

    E.g :help paste
