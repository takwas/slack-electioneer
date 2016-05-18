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
import os
import sys
import json
import textwrap
import time

# library imports
from slackclient import SlackClient
#from redis_cache import SimpleCache

# local imports
from wrappers import Instruction, Vote
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
        #self.waiting = False
        self.team_members = []
        self.db = models
        #self.chn_msgs_cache = SimpleCache(10, expire=self.config.CACHE_EXPIRY)
        #self.postts_candidate_cache = SimpleCache(30, expire=self.config.CACHE_EXPIRY)

        try:
            print 'Connecting to database...' #DEBUG
            self.connect_db()
            print 'Connected to database!!' #DEBUG
        except:
            print 'Database connection failed!\nExiting...'
            sys.exit(1)

        self.connect_rtm()
        self.join_voting_channels()

    # Synchronize needed Slack data with DB
    def sync_slack_members_with_db_profiles(self):
        if not self.team_members:
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
        # MARK TODO: Fix this
        # Find any DB `Profile` whose Slack account
        # has been deleted and delete their DB profile
        # for profile in self.db.session.query(self.db.Profile).all():
        #     if self.team_members.get(profile.userid) is None:
        #         self.db.session.delete(profile)

        # save all changes
        try:
            self.db.session.commit()
        except:
            print 'Failed to commit DB transactions' #DEBUG
            self.db.session.rollback()

    # Load all Slack members' info into memory
    def load_all_members(self):
        if not self.team_members:
            response = self.api_call('users.list')
            self.team_members = response.get('members')
    
    def load_stats(self):
        self.stats = dict()
        for office in self.db.session.query(self.db.Office).all():
            self.stats[office.channel] = {
                'office' : office.name,
                'topic' : office.topic,
                'purpose' : office.purpose,
                'live_ts' : office.live_ts,
                'log_ts' : office.log_ts,
                'candidates' : {
                    x.candidate.userid : {
                        'post_ts' : x.post_ts,
                        'votes_count' : len(x.votes)
                    } for x in office.candidacies
                }
            }
        if not self.stats:
            print 'No data found! Run setup first.'
            sys.exit(1)

    # Do initial data loading
    def load_data(self):
        self.sync_slack_members_with_db_profiles()
        self.load_stats()
        self.userid = self.get_userid(self.username)
        for channel in self.voting_channels:
            self.clear_channel(channel, clean=False)
        #self.load_all_members()

    # Setup database for first time use
    def setup_db(self):

        def populate_db():
            # Save basic of Slack team members to DB profiles
            print 'Starting sync...' # DEBUG
            self.sync_slack_members_with_db_profiles()
            print 'Done syncing!' # DEBUG
            # Save stats elections and offices in DB
            for key, value in self.stats.iteritems():
                self.db.session.add(
                    self.db.Office(
                            name=value.get('office'),
                            channel=key,
                            topic=value.get('topic'),
                            purpose=value.get('purpose'),
                            log_ts='', # to be assigned when log is created
                            live_ts='' # to be assigned when live msg is created
                    )
                )
            # Register candidates
            for key, value in self.stats.iteritems():
                candidates = value.get('candidates')
                for candidate, data in candidates.iteritems():
                    self.db.session.add(
                        self.db.Candidacy(
                            office_id=self.db.session.query(self.db.Office).filter_by(channel=key).first().id,
                            candidate_id=self.db.session.query(self.db.Profile).filter_by(userid=candidate).first().id,
                            post_ts=data.get('post_ts')
                        )
                    )


        print 'Preparing database...' #DEBUG
        db_filename = self.config.DATABASE_URL[self.config.DATABASE_URL.rfind('/')+1:]
        os.unlink(db_filename)
        self.connect_db()
        print 'Database ready!' #DEBUG

        populate_db()
        self.db.session.commit()

        

    # Create and initialize database
    def connect_db(self):
        self.db.initdb(self.config.DATABASE_URL)

    # Connect to Slack's RTM API
    def connect_rtm(self):
        print 'Votebot connecting to RTM API...' #DEBUG
        if self.rtm_connect():
            print 'Votebot connected!' #DEBUG
        else:
            print 'Votebot failed to connect!' #DEBUG
    
    # Make bot join voting channels
    def join_voting_channels(self):
        print 'Joining voting channels...!' #DEBUG
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
    def listen(self):
        print 'Votebot Listening...' #DEBUG
        while True:
            for event in self.rtm_read():
                # do something with RTM API event
                #print event # DEBUG

                if event.get('type') == 'message' and event.get('text') is not None:
                    if event.get('channel') in self.voting_channels:
                    #and event.get('user')!=self.userid and event.get('username')!='slackbot':
                        # Guard against UnicodeEncodeError
                        #print event
                        event['text'] = event.get('text').encode('utf-8')
                        self.log_msg(
                            text='{name} wrote:\t{msg}'.format(
                                name=event.get('user'),
                                msg=event.get('text')
                            ),
                            channel=event.get('channel')
                        )
                        if event.get('user') in self.masters.values():
                            self.parser.parse_msg(msg=event.get('text'), event=event)
                        else:
                            if event.get('user') != self.userid:
                                self.delete_msg(event.get('channel'), event.get('ts'))

                elif event.get('type') == 'reaction_added' and event.get('item').get('channel') in self.voting_channels:
                    
                    if event.get('reaction') == self.vote_symbol:
                        vote = Vote(
                            voter_userid=event.get('user'),
                            candidate_userid=self.get_candidate_from_post_ts(
                                event.get('item').get('channel'),
                                event.get('item').get('ts')
                            ),
                            channel=event.get('item').get('channel')
                        )
                        if self.validate_vote(vote):
                            self.save_vote(vote)
                            print 'here'
                            self.update_live_stats(event.get('item').get('channel'))
                            print 'here2'
                        else:
                            self.log_msg(
                                text=textwrap.dedent(
                                    '''
                                    Wrong reaction:
                                    {name}: Added {reaction}
                                    '''.format(
                                        name=event.get('user'),
                                        reaction=event.get('reaction')
                                    )
                                ),
                                channel=event.get('channel')
                            )
                    elif event.get('type') == 'reaction_added':
                        self.log_msg(
                            text=textwrap.dedent(
                                '''
                                Wrong reaction:
                                {name}: Added {reaction}
                                '''.format(
                                    name=event.get('user'),
                                    reaction=event.get('reaction')
                                )
                            ),
                            channel=event.get('channel')
                        )
                elif event.get('type') == 'reaction_removed':
                    self.log_msg(
                        text=textwrap.dedent(
                            '''
                            Wrong reaction:
                            {name}: Removed {reaction}
                            '''.format(
                                name=event.get('user'),
                                reaction=event.get('reaction')
                            )
                        ),
                        channel=event.get('channel')
                    )

    # Parse vote object and save data to DB
    def save_vote(self, vote_obj):
        voter_profile = self.db.session.query(self.db.Profile).filter_by(userid=vote_obj.voter_userid).first()
        office_voted = self.db.session.query(self.db.Office).filter_by(channel=vote_obj.channel).first()
        candidate_voted = self.db.session.query(self.db.Profile).filter_by(userid=vote_obj.candidate_userid).first()
        candidacy = self.db.session.query(self.db.Candidacy).filter_by(office_id=office_voted.id, candidate_id=candidate_voted.id).first()
        self.db.session.add(
            self.db.Vote(
                voter_id=voter_profile.id,
                candidacy_id=candidacy.id
            )
        )
        self.stats.get(vote_obj.channel).get('candidates').get(vote_obj.candidate_userid)['votes_count'] += 1
        self.db.session.commit()

    # Validate a `Vote` object
    # Check against double voting
    def validate_vote(self, vote_obj):
        profile = self.db.session.query(self.db.Profile).filter_by(userid=vote_obj.voter_userid).first()
        prev_votes = self.db.session.query(self.db.Vote).filter_by(voter_id=profile.id).all()
        for vote in prev_votes:
            if vote.candidacy.office.channel==vote_obj.channel:
                return False
        return True

    # Vote for candidate with id `candidate_userid` in voting channel
    # with `channel_name_or_id` by adding a checkmark to their
    # listed profile
    def vote_for(self, candidate_userid, channel_name_or_id):
        #try:
        msg_ts = self.stats.get(channel_name_or_id).get('candidates').get(candidate_userid).get('post_ts')
        vote_obj = Vote(
            voter_userid=self.userid,
            candidate_userid=candidate_userid,
            channel=channel_name_or_id
        )
        self.save_vote(vote_obj)
        # except:
        #     msg_ts = None
        #     print 'Error voting!' # DEBUG
        
        if msg_ts is not None:
            return self.api_call('reactions.add', name=self.vote_symbol, channel=channel_name_or_id, timestamp=msg_ts)
        else:
            return None

    def get_candidate_from_post_ts(self, channel, post_ts):
        #candidate_userid = postts_candidate_cache.get(post_ts)
        #if candidate_userid is None:
        candidates = self.stats.get(channel).get('candidates')
        print '%r' % candidates
        for candidate_userid, value in candidates.iteritems():
            if value.get('post_ts') == post_ts:
        #        postts_candidate_cache.set(post_ts, candidate)
                return candidate_userid
        

    # MARK
    # def save_candidates(self, names, channel_id):
    #     candidate_names = [self.parse_mention(x.strip()) for x in names.split(',')]
    #     for name in candidate_names:
    #         if channel in self.voting_channels:
    #             userid = self.get_userid(name)
    #             self.stats.get(channel).get('candidates')[name] = \
    #                 Candidate(userid, self.get_userbio(userid))

    # Format userid into a mention
    def format_user_mention(self, userid):
        return '<@{userid}>'.format(userid=userid)

    # Extract userid from a mention
    def parse_user_mention(self, mention):
        return mention.strip('<@>')

    # Post `text` as message to channel with `channel_name_or_id`
    def post_msg(self, text, channel_name_or_id):
        response = self.api_call('chat.postMessage',
            text=text,
            channel=channel_name_or_id,
            as_user=True # `True`, so it makes sure to post using the bot's authed identity
        )
        return response

    # Updates message with given timestamp (`msg_ts`) in `channel`
    # Accepts a callback (`callback`) that contains instructions
    # for processing the old text and generating the desired
    # new text for updating the message
    def edit_msg(self, channel, msg_ts, callback):
        channel_history = self.api_call('channels.history',
            channel=channel,
            latest=msg_ts,
            inclusive=True
        )
        for message in channel_history.get('messages'):
            if message.get('ts')==msg_ts:
                prev_text = message.get('text')
                break
        new_text = str()
        
        if prev_text is not None:
            new_text = callback(prev_text)
        print prev_text
        print new_text

        return self.api_call('chat.update',
            ts=msg_ts,
            text=new_text,
            channel=channel,
            as_user=True
        )

    # Appends `text` to a message with given timestamp (`msg_ts`)
    # in `channel` using a delimiter (`delimiter`)
    def append_msg(self, text, channel, msg_ts, delimiter='\n'):
        return self.edit_msg(
            channel, msg_ts, callback=lambda x:'{x}{delim}{txt}'.format(x=x, delim=delimiter, txt=text)
        )

    # Appends a log message (`text`) to a channel's (`channel`)
    # log message
    def log_msg(self, text, channel):
        # msg_ts = self.stats.get(channel).get('log_ts')
        # delimiter = '\n{}\n'.format(time.time())
        # return self.append(text, channel, msg_ts, delimiter)

        # self.api_call('files.upload',
        #     filename='log.txt',
        #     title='Log',
        #     channel=channel,
        #     content=textwrap.dedent(
        #         '''
        #         Hello Log!

        #         '''
        #     )
        # )
        with open('log_{}.txt'.format(channel), 'a') as f:
            f.write('{}\n'.format(text))

    # Gets the Slack userid of member with `username`
    def get_userid(self, username):
        userid = None        
        for member in self.team_members:
            if member.get('name')==username:
                userid = member.get('id')
                break
        return userid

    # MARK
    def get_userbio(self, userid):
        bio = textwrap.dedent(
            '''
            Candidate: {mention}
            > For: {office}
            > Name: *{real_name} *
            > Title: _{title} _
            
            (_Vote by clicking on the green white checkmark below_)
            '''.format(
                mention=self.format_user_mention(userid),
                real_name=user['profile']['real_name'],
                title=user['profile']['title']
            )
        )
        return bio

    # MARK    
    def get_user(self, userid):
        response = self.api_call('users.info', user=userid)
        return response.get('user')

    # Adds a user's profile (as candidate) to the channel given
    def add_candidate(self, userid, channel_name_or_id):
        user = self.get_user(userid)
        real_name = user['profile']['real_name']
        title = user['profile']['title']
        response = self.post_msg(
            text=textwrap.dedent(
                '''
                Candidate: {mention} for *{office}* :heavy_check_mark:
                > Name: *{real_name}*
                > Title: _{title} _
                '''.format(
                    mention=self.format_user_mention(userid),
                    real_name=real_name,
                    title=title,
                    office=self.stats.get(channel_name_or_id).get('office')
                )
            ),
            channel_name_or_id=channel_name_or_id
        )
        self.stats.get(channel_name_or_id).get('candidates').get(userid)['post_ts'] = response.get('ts')
        profile = self.db.session.query(self.db.Profile).filter_by(userid=userid).first()
        office = self.db.session.query(self.db.Office).filter_by(channel=channel_name_or_id).first()
        self.db.session.query(self.db.Candidacy).filter_by(
            office_id=office.id,
            candidate_id=profile.id
        ).first().post_ts=response.get('ts')
        self.db.session.commit()

        try:
            if self.config.MODE == 'testing':
                if not real_name or not title:
                    self.post_msg(
                        text='{mention}: *You should update your profile.*'.format(mention=self.format_user_mention(userid)),
                        channel_name_or_id=channel_name_or_id
                    )
                else:
                    self.post_msg(
                        text='{mention}: *Your profile looks good.* :simple_smile:'.format(mention=self.format_user_mention(userid)),
                        channel_name_or_id=channel_name_or_id
                    )
        except:
            pass
        return response

    # load all messages from channel with `channel_name_or_id`;
    # uses a cache
    def get_messages(self, channel_name_or_id):
        # messages = self.chn_msgs_cache.get(channel_name_or_id)
        # print 'HERE %r' %messages
        # if messages is None:
        response = self.api_call(
            'channels.history', channel=channel_name_or_id
        )
        messages = response.get('messages')
        #    print 'HERE2 %r' %messages
        #    self.chn_msgs_cache.store(channel_name_or_id, messages)
        return messages

    # MARK
    def get_stats(self, channel_name_or_id):
        messages = self.get_messages(channel_name_or_id)
        candidates_profiles = []
        stat_report = None
        office_id=self.db.session.query(self.db.Office).filter_by(channel=channel_name_or_id).first().id

        if messages is not None:
            for message in messages:
                if message.get('user') == self.userid and \
                    message.get('text').strip().startswith('Candidate'):
                    candidates_profiles.append(message)
            
            if candidates_profiles:
                stat_report = textwrap.dedent(
                    '''
                    *Live Stats*
                    > 
                    '''
                )
                for candidate_profile in candidates_profiles:
                    user_mention = candidate_profile.get('text').strip().split('\n')[0].split()[1].strip()
                    userid = self.parse_user_mention(user_mention)
                    profile = self.db.session.query(self.db.Profile).filter_by(userid=userid).first()
                    candidacies = profile.candidacies
                    for candidacy in candidacies:
                        if candidacy.office_id == office_id:
                            votes_count = len(candidacy.votes)
                            print 'Count %d' %votes_count
                    self.stats[channel_name_or_id]['candidates'][userid]['votes_count'] = votes_count

                    stat_report += ' {mention}: `{count}` | '.format(
                        mention=user_mention,
                        count=votes_count
                    )
        return stat_report
    
    # Show live updates of election results
    def update_live_stats(self, channel_name_or_id):
        stats = self.get_stats(channel_name_or_id)
        ts = self.stats.get(channel_name_or_id).get('live_ts')
        print self.edit_msg(channel_name_or_id, msg_ts=ts, callback=lambda x: stats)


    # Delete message with timestamp `msg_ts` from `channel`
    def delete_msg(self, channel_name_or_id, msg_ts):
        response = self.server.api_requester.do(
            self.admin_token,
            'chat.delete', # the API method to call
            dict(channel=channel_name_or_id, ts=msg_ts)
        )
        return json.loads(response.text)

    # Clear all messges in channel
    def clear_channel(self, channel_name_or_id, clean=True):
        messages = self.get_messages(channel_name_or_id)
        for message in messages:            
            if not clean:
                if message.get('user')==self.userid:
                    continue
            self.delete_msg(channel_name_or_id, msg_ts=message.get('ts'))

    # Set/change the topic of channel with `channel_name_or_id`
    def set_channel_topic(self, text, channel_name_or_id):
        return self.api_call('channels.setTopic', topic=text, channel=channel_name_or_id)

    # Set/change the purpose of channel with `channel_name_or_id`
    def set_channel_purpose(self, text, channel_name_or_id):
        return self.api_call('channels.setPurpose', purpose=text, channel=channel_name_or_id)

    def pin_msg_to_channel(self, channel_name_or_id, msg_ts):
        return self.api_call('pin.add', channel=channel_name_or_id, timestamp=msg_ts)