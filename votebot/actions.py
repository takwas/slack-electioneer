# -*- coding: utf-8 -*-
"""
    votebot.actions
    ~~~~~~~~~~~~~~~

    Actions are the `functions` that perform the different functionalities
    of a bot. An action takes a message as argument and returns a
    `Response` object.

    List of actions currently supported:

        do_help
        do_about
        do_link
        do_masters
        do_override


    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""

# standard library imports
import textwrap

# local imports
import bot
import utils


class Response(object):
    """
    A `Response` object encapsulates a message as a newline-delimited
    `list` of `strings`.

    An `action` will return a `Response` object.

    In creating a `Response` object, a single message `string` can be
    passed, but will be split into a `list` delimited by newlines
    internally.
    """

    def __init__(self, messages=[], channel=None, private=False, \
                    general=False):
        """
        Constructor method for a Response object.

        Accepts the message for this Response as a list
        or a string delimited by newlines. If there are
        no newlines, there will be only one item in the
        list of messages.
        """
        # If a string is passed
        if messages is not None and isinstance(messages, str):
            self.messages = messages.split('\n')
        # If an iterable (list or tuple) is passed
        elif messages is not None and (isinstance(messages, list) or
                                        isinstance(messages, tuple)):
            self.messages = messages
        else:
            raise TypeError(messages+' is not iterable!')
        self.channel = channel
        self.is_private = private
        self.is_general = general

    def add_message(self, msg):
        """
        Add a message to list of messages contained
        in this Response object.
        """
        self.messages.append(msg)

    def get_response(self):
        """
        Get the list of messages contained in this Response
        object in the order they were added.
        """
        return self.messages


# Action functions

def do_help(bot, msg=None, **kwargs):
    """
    Show help information for command passed through `msg`.

    Indicate if the command does not exist.
    """
    channel = kwargs.get('event').get('channel')
    # Show help message if command was entered without args
    if msg is None or msg == '' or msg == ' ':

        def format_cmds():
            """
            Inner helper function.

            This should give an output of the form:
                :help, :about, :clear, :initiate, :admins
            """
            from commands import cmds

            return ':' + ', :'.join(sorted(cmds.keys()))

        return bot.post_msg(
            text=textwrap.dedent(
                """
                *Showing general help.*

                List of commands:
                    {cmds}

                For help on a command, type:
                    :help [command]

                E.g :help paste
                """.format(cmds=format_cmds())
            ),
            channel_name_or_id=channel
        )

    elif utils.is_valid_cmd(msg):
        from commands import cmds
        return bot.post_msg(
            text=cmds.get(msg).help_text,
            channel_name_or_id=channel
        )

    else:
        return Response(
                "No help for '{cmd}'.\nType ':help' (without the quotes) for "
                "a list of commands.".format(cmd=msg)
                )


def do_about(bot, msg, **kwargs):
    """
    Return some 'about' information about the receiving bot.
    """
    channel = kwargs.get('event').get('channel')
    return bot.post_msg(
        text=bot.about,
        channel_name_or_id=channel
    )

    return Response(bot.about)

def do_clear(bot, msg, **kwargs):
    channel = kwargs.get('event').get('channel')
    # Clear channel
    bot.clear_channel(channel)
    return True    

def do_initiate(bot, msg, **kwargs):
    """
    Set channel up for an election
    """
    channel = kwargs.get('event').get('channel')
    instructions = textwrap.dedent(
        '''
        :cop:I name is *{name}*, your election police

        
        :grey_question:*How to Vote:*
        Voting in here is simple. Each candidate's profile is listed with a white-on-green checkmark beneath their profile. All you have to do is *click the checkmark once* for your preferred candidate.


        :warning:*Rules*:
        1. *Only your first vote counts*. Regardless of the count on checkmark, only your first vote is valid and recorded. Subsequent votes or attemps to remove already cast ballots would be ignored.

        2. *Do not try to post any messages in this channel* as such messages would be deleted immediately.

        Now...
        > _Be Nice, Be Respectful, Be Civil_ :simple_smile:


        I will now list the candidates. Happy Voting :simple_smile:

        '''.format(
            name=bot.username,
        )
    )
    #:sleuth_or_spy:These people can instruct me: *{admins}*
    #admins=', '.join([bot.format_user_mention(x) for x in bot.masters.values()])

    # Clear channel
    bot.clear_channel(channel)
    print 'DEBUG output' # DEBUG
    # Set channel topic
    bot.set_channel_topic(bot.stats.get(channel).get('topic'), channel)
    # Show instructions
    instruction_response = bot.post_msg(text=instructions, channel_name_or_id=channel)
    # Set channel purpose
    bot.set_channel_purpose(bot.stats.get(channel).get('purpose'), channel)
    # Pin message to channel
    bot.pin_msg_to_channel(channel, instruction_response.get('ts'))

    # Add candidates for this office
    for userid, data in bot.stats.get(channel).get('candidates').iteritems():
        bot.add_candidate(userid, channel)
        bot.vote_for(userid, channel)

    live_stats = bot.get_stats(channel)
    if live_stats is not None:
        response = bot.post_msg(
            text=live_stats,
            channel_name_or_id=channel
        )
        bot.stats.get(channel)['live_ts'] = response.get('ts')

    bot.log_msg('Channel{} prepared for voting.'.format(channel), channel)

    return True
    #return Response(bot.about)


# def do_link(bot, msg, **kwargs):
#     """
#     Returns the URL to the webpage of the user whose nick is contained
#     as parameter in `msg`.
#     """
#     # Show help message if command was entered without args
#     if msg is None or msg == '' or msg == ' ':
#         return do_help(bot=bot, msg='link')

#     links_data = utils.reload_links('data/links.json')
#     response = Response(links_data.get(msg,
#                         'google.com/?search={query}'.format(query=msg)))
#     return response

# def do_log(bot, msg, **kwargs):
#     """
#     This will perform logging.

#     The logging is configurable based on the parameters in `msg`.
#     """
#     # Show help message if command was entered without args
#     if msg is None or msg == '' or msg == ' ':
#         return do_help(bot=bot, msg='log')

#     # THIS IS NOT FULLY IMPLEMENTED YET

#     now = datetime.datetime.now()
#     filename = "logs/Logs-%s.txt" % now.strftime("%Y-%m-%d-%H-%M")
#     logger = MessageLogger(open(self.filename, "a"))

#     logger.log("[## Class Started at %s ##]" %
#                 time.asctime(time.localtime(time.time())))
#     user = user.split('!', 1)[0]
#     self.logger.log("<%s> %s" % (user, msg))
#     self.islogging = True

#     response = Response("Now logging in file {filename}".format(
#                         filename="some_filename"))
#     return response


def do_masters(bot, msg, **kwargs):
    """
    Return the usernames of those who currently have admin priviledges over
    the bot receiving this message.
    """
    channel = kwargs.get('event').get('channel')
    bot.post_msg(
        text='My admins are: {admins}'.format(
            admins=', '.join([bot.format_user_mention(x) for x in bot.masters.values()]),
            channel_name_or_id=channel
        )
    )
    return True


def do_override(bot, msg, **kwargs):
    """
    The text in `msg` will be rebroadcasted by the bot receiving this
    message in the specified channel.

    It is a sort of manual override.
    """
    # Show help message if command was entered without args
    if msg is None or msg == '' or msg == ' ':
        return do_help(bot=bot, msg='ctrl', **kwargs)

    # Get the name of the channel to post `msg` to
    channel, msg = parse_channel_name(msg)
    channel = kwargs.get('event').get('channel')
    # Is there a message to post?
    if len(msg)>0:
        ## The initial space indicates that the message is a manual override.
        #response = Response(' '+msg, general=True, channel=channel)
        bot.post_msg(
            text=msg,
            channel_name_or_id=channel
        )
    return True


# def do_submit(bot, msg, **kwargs):
#     """
#     This will enable a user provide a message that will be saved by the
#     receiving bot, for use by the developers.

#     For example a message mentioning a bug, or some other feedback.
#     """
#     # Show help message if command was entered without args
#     if msg is None or msg == '' or msg == ' ':
#         return do_help(bot=bot, msg='submit')

#     # IMPLEMENT SAVE msg
#     response = Response("Thank you. I have received your submission.".format(
#                         filename="some_filename"))
#     return response



# Helper functions

# Extract name of channel from message arguments
def parse_channel_name(msg):
    import utils

    channel_name_start = msg.find('=')+1
    channel_name_end = msg.find(' ')
    channel = msg[channel_name_start:channel_name_end]
    channel = utils.verify_channel(channel)
    msg = msg[channel_name_end:].strip()
    return channel, msg