# -*- coding: utf-8 -*-
"""
    votebot.votebot
    ~~~~~~~~~~~~~~~

    Bot (Slack client) module.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""
# standard library imports
import sys
import json
import textwrap
import time

# library imports
from slackclient import SlackClient
from redis_cache import SimpleCache

# local imports
from commands import cmds
from parser import ArgsParser
import utils
import models


class VoteBot(SlackClient):

    # Create bot instance
    def __init__(self, config):
        SlackClient.__init__(self, config.TOKEN)
        self.config = config
        self.admin_token = config.ADMIN_TOKEN
        self.username = config.BOT_NAME
        self.masters = config.BOT_ADMINS
        self.vote_symbol = config.VOTE_SYMBOL
        self.stats = config.STATS
        self.voting_channels = self.stats.keys()
        self.sourceURL = config.SOURCE_URL
        self.about = config.ABOUT
        self.parser = ArgsParser(bot=self)
        self.waiting = False
        self.team_members = []
        self.userid = self.get_userid(self.username)
        self.db = models
        self.chn_msgs_cache = SimpleCache(10, expire=self.config.CACHE_EXPIRY)

        try:
            print 'Preparing database...' #DEBUG
            self.connect_db()
            print 'Database ready!' #DEBUG
        except:
            print 'Database connection/initialization failed!\nExiting...'
            sys.exit(1)

        self.load_all_members()
        self.load_data()
        self.connect_rtm()
    

    def sync_slack_members_with_db_profiles(self):
        if not team_members:
            self.load_all_members()

        # Find any new Slack team member
        # and add their profile to the DB
        for member in self.team_members:
            if self.db.session.query(self.db.Profile).filter_by(userid=member.get('id')).first() is None:
                self.db.session.add(
                    self.db.Profile(
                        userid=member.get('id'),
                        username=member.get('name'),
                        title=member.get('profile').get('title'),
                    )
                )
        # Find any DB `Profile` whose Slack account
        # has been deleted and delete their DB profile
        for profile in self.db.session.query(self.db.Profile).all():
            members.get(profile.userid) is None:
            self.db.session.delete(profile)

        # save all changes
        try:
            session.commit()
        except:
            print 'Failed to commit DB transactions' #DEBUG
            session.rollback()
    
    def load_stats(self):
        self.stats = dict()
        for office in self.db.session.query(self.db.Office).all():
            self.stats[office.channel] = {
                'name' : office.name,
                'topic' : office.topic,
                'purpose' : office.purpose,
                'live_ts' : office.live_ts,
                'log_ts' : office.log_ts,
                'candidates' : {
                    x.candidate.userid : {'post_ts' : x.post_ts} for x in office.candidacies
                }
            }

    def setup_db(self):
        self.db.initdb(self.config.DATABASE_URL)
        populate_db()
        session.commit()

        def populate_db():
            # Save basic of Slack team members to DB profiles
            self.sync_slack_members_with_db_profiles()
            # Save stats elections and offices in DB
            for key, value in self.stats.iteritems():
                self.db.session.add(
                    self.db.Office(
                            name=value.get(office),
                            channel=key,
                            topic=value.get(topic),
                            purpose=value.get(purpose),
                            log_ts='', # to be assigned when log is created
                            live_ts='' # to be assigned when live msg is created
                    )
                )


    def connect_db(self):
        models.initdb(self.config.DATABASE_URL)

    def connect_rtm(self):
        # Make bot connect to the RTM API
        if self.rtm_connect():
            print 'Votebot connected! Listening...'
        else:
            print 'Votebot failed to connect!'

    def load_data(self):
        users = self.db.session.query(self.db.Profile).all()
        print users

    def listen(self):
        # Make bot join voting channels
        for channel in self.voting_channels:
            self.server.join_channel(channel)
            channel_info = self.api_call('channels.info', channel=channel)
            try:
                if channel_info is not  None:
                    channel_name = '#' + channel_info.get(\
                        'channel', {}).get('name')
                if channel_name is not None:
                    print 'Joined channel: {}'.format(channel_name) #DEBUG
            except:
                print 'Error joining channel: {}'.format(channel) #DEBUG

        # Begin listening for JSON formatted RTM API messages/events
        while True:
            for event in self.rtm_read():
                # do something with RTM API message/event
                print event

                if event.get('type') == 'message':
                    if event.channel in self.voting_channels and \
                        event.user in self.masters.values():
                        bot.parser.parse_msg(message)


                # if message.get('text') == 'stat':
                #     tak = self.masters.get('acetakwas')
                #     #self.add_candidate(tak, message.get('channel'))
                #     msg = self.get_stats(message.get('channel'))
                #     print msg
                #     self.post_msg(msg, message.get('channel'))

                # # if message.get('user') == self.masters.get('acetakwas'):
                #     response = self.delete_msg(
                #         message.get('channel'), message.get('ts')
                #     )                            
    
    def save_candidates(self, names, channel_id):
        candidate_names = [self.parse_mention(x.strip()) for x in names.split(',')]
        for name in candidate_names:
            if channel in self.voting_channels:
                userid = self.get_userid(name)
                self.stats.get(channel).get('candidates')[name] = \
                    Candidate(userid, self.get_userbio(userid))

    def validate_vote(self, voter_obj):
        profile = self.db.session.query(self.db.Profile).filter_by(userid=voter_obj.voter_userid).first()
        prev_votes = self.db.session.query(self.db.Vote).filter_by(voter_id=profile.id).all()
        for vote in prev_votes:
            if vote.candidacy.office.channel==voter_obj.channel
                return False
        return True

    def load_all_members(self):
        if not self.team_members:
            response = self.api_call('users.list')
            self.team_members = response.get('members')

    def get_userid(self, username):
        userid = None        
        for member in self.team_members:
            if member.get('name')==username:
                userid = member.get('id')
        return userid

    def get_userbio(self, userid):
        bio = textwrap.dedent(
            '''
            Candidate: {mention}
            > Name: *{real_name}*
            > Title: _{title} _
            
            (_Vote by clicking on the green white checkmark below_)
            '''.format(
                mention=self.format_user_mention(userid),
                real_name=user['profile']['real_name'],
                title=user['profile']['title']
            )
        )
        return bio

    def get_user(self, userid):
        response = self.api_call('users.info', user=userid)
        return response.get('user')

    def format_user_mention(self, userid):
        return '<@{userid}>'.format(userid=userid)

    def parse_user_mention(self, mention):
        return mention.strip('<@>')

    def add_candidate(self, userid, channel_name_or_id):
        user = self.get_user(userid)
        self.post_msg(
            msg=textwrap.dedent(
                '''
                Candidate: {mention}
                > Name: *{real_name}*
                > Title: _{title} _
                
                (_Vote by clicking on the green white checkmark below_)
                '''.format(
                    mention=self.format_user_mention(userid),
                    real_name=user['profile']['real_name'],
                    title=user['profile']['title'])
            ),
            channel_name_or_id=channel_name_or_id
        )

    def post_msg(self, msg, channel_name_or_id):
        response = self.api_call('chat.postMessage',
            text=msg,
            channel=channel_name_or_id,
            as_user=True # `True`, so it makes sure to post using the bot's authed identity
        )
        return response

    def edit_msg(self, channel, msg_ts, callback):
        prev_text, new_text = self.get_message(channel, msg_ts), ''
        if prev_text is not None:
            new_text = callback(prev_text)
        return self.api_call('chats.update', channel=channel, text=new_text)

    def append_msg(self, msg, channel, msg_ts, delimiter='\n'):
        return self.edit_msg(
            channel, msg_ts, callback=lambda x:return x + delimiter + msg
        )

    def log_msg(self, msg, channel):
        msg_ts = self.stats.get(channel).get('log_ts')
        delimiter = '\n{}\n'.format(time.time())
        return self.append(msg, channel, msg_ts, delimiter)

    # load all messages from a channel; uses a cache
    def get_messages(self, channel_name_or_id):
        messages = self.chn_msgs_cache.get(channel_name_or_id)
        if messages is None:
            response = self.api_call(
                'channels.history', channel=channel_name_or_id
            )
            messages = response.get('messages')
            self.chn_msgs_cache.store(channel_name_or_id, messages)
        return messages

    def get_stats(self, channel_name_or_id):
        messages = self.get_messages(channel_name_or_id)
        candidates_profiles = []
        stat_report = None

        if messages is not None:
            for message in messages:
                if message.get('user') == self.userid and \
                    message.get('text').strip().startswith('Candidate'):
                    candidates_profiles.append(message)
            
            if candidates_profiles:
                stat_report = ''
                for candidate_profile in candidates_profiles:
                    stat_report += '\n{name}: *{count}*'.format(
                        name=candidate_profile.get('text').strip().split('\n')[0].split(':')[1].strip(),
                        count=candidate_profile.get('reactions')[0].get('count')
                    )
        return stat_report

    def vote_for(userid, office):
        try:
            channel = self.config.OFFICES.get(office.lower()).get('channel')
        except:
            return

        #self.api_call('reaction.add', ts)

    def delete_msg(self, channel_name_or_id, msg_ts):
        response = self.server.api_requester.do(
            self.admin_token,
            'chat.delete', # the API method to call
            dict(channel=channel_name_or_id, ts=msg_ts)
        )
        return json.loads(response.text)

    def privmsg(self, user, channel, msg):
            """
            This will get called when the bot receives a message.

            :param user: absolute ID of user who sent the message. A typical
                        ID would look like this: sawkat!~sawkat@100.110.120.6
            :param channel: channel where the message was sent. The `channel`
                            is a channel if the message was sent in a
                            channel. The `channel` is the bot's nick if the
                            message

                            was sent as a private message
            :param msg: the message string that was sent
            """
            # Get nick of message sender
            user = user.split('!', 1)[0]

            user_is_admin = user in self.masters

            # Is this a private message to me?
            if channel == self.nickname:
                room = user
                response = self.parser.parse_msg(msg, sender=user)
            # Or is this a message directed at me from a channel?
            elif msg.startswith(self.nickname):
                room = channel
                # remove the nick and parse the message
                response = self.parser.parse_msg(msg[msg.find(' ')+1:], sender=user)

            # Process a response if allowed to talk
            if not self.stealth:
                msg = ''
                for line in response.get_response():
                    msg += line+'\n'

                if response.is_general:
                    if response.channel is not None:
                        self.msg_channel(response.channel, msg)
                elif room == user or (room == channel and response.is_private):
                    self.msg_user(user, msg)
                elif room == channel and not response.is_private:
                    self.msg_user_in_channel(channel, user, msg)


# Object to wrap received commands
class Instruction(object):

    def __init__(self, sender_userid, msg, channel):
        self.sender_userid = sender_userid
        self.msg = msg
        self.channel = channel


# Object to wrap received voting data
class Vote(object):

    def __init__(self, voter_userid, candidate_userid, channel):
        self.voter_userid = voter_userid
        self.candidate_userid = candidate_userid
        self.channel = channel