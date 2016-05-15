
A Slack bot used for voting committee members in the [Slack team](https://pythonnigeria.slack.com) of the [Nigeria Python Users Group](https://wiki.python.org/moin/LocalUserGroups#Nigeria).

To run:

Install dependencies with:

```bash
$ pip install -r requirements.txt
```

Go to your Slack team.
Create a Slack bot and retrieve a token.
Store your slack token in an environment variable like so:

```bash
$ export SLACK_TOKEN=your_slack_token
$ export VOTEBOT_CONFIG_MODE=your_config_mode # Options are: dev, deploy, test
```

Run bot with:

```bash
$ python run.py
```
