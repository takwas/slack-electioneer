# -*- coding: utf-8 -*-
"""
    votebot.commands
    ~~~~~~~~~~~~~~~~

    Commands recognisable by bot.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""

# standard library imports
import textwrap

# local imports
import actions


class Command(object):
    """
    This provides a wrapper object for a command. Each command that can
    be executed on the bot has it's own set of properties which are
    contained in this class.
    """

    def __init__(self, cmd, callback, help_text):

        # The command text for this command
        self.cmd = cmd

        # The callback function to execute when this command is run
        self.callback = callback

        # A text containing help information on how to use this command
        self.help_text = help_text

    def __repr__(self):
        return 'Command: <{cmd}>'.format(cmd=self.cmd)

    def execute(self, **kwargs):
        """
        Execute this command by running the callback function created
        with it. Return the result of the function afterwards.
        """
        return self.callback(**kwargs)


# A mapping of commands to their respective Command objects
#
# Currently included commands:
#     :help :about :inbox :link :log :masters :paste :ctrl
#     :whatdidimiss :resource :submit
cmds = {
    'help' : Command(cmd='help', callback=actions.do_help,
                        help_text=textwrap.dedent(
                            """
                            Usage:

                                U1:\t:help
                                    Show general help.

                                U2:\t:help <command>
                                    Show help for <command>. Use <U1> for a
                                    list of valid commands.
                            """
                            )
                            ),
    'about' : Command(cmd='about', callback=actions.do_about,
                        help_text=textwrap.dedent(
                            """
                            Usage:

                                U1:\t:about
                                    Show 'about' information for this bot.
                            """
                            )
                            ),
    'link' : Command(cmd='link', callback=actions.do_link,
                        help_text=textwrap.dedent(
                            """
                            Usage:

                                U1:\t:link
                                    Show help for this command.

                                U2:\t:link list
                                    Show a list of available link titles.

                                U3:\t:link <link_title>
                                    Show URL for <link_title>.
                            """
                            )
                            ),
    # 'log' : Command(cmd='log', callback=actions.do_log,
    #                     help_text=textwrap.dedent(
    #                         """
    #                         Usage:

    #                             U1:\t:log
    #                                 Show help for this command.
    #                         """
    #                         )
    #                         ),
    'boss' : Command(cmd='boss', callback=actions.do_masters,
                        help_text=textwrap.dedent(
                            """
                            Usage:

                                U1:\t:boss
                                    Show the users who can control this bot.
                            """
                            )
                            ),
    'ctrl' : Command(cmd='ctrl', callback=actions.do_override,
                        help_text=textwrap.dedent(
                            """
                            Usage:

                                U1:\t:ctrl
                                    Show help for this command.
                                U2:\t:ctrl :chan=<channel> <msg>
                                    Make the bot say <msg> in <channel>.
                            """
                            )
                            )
    # 'submit' : Command(cmd='submit', callback=actions.do_submit,
    #                     help_text=textwrap.dedent(
    #                         """
    #                         Usage:

    #                             U1:\t:submit
    #                                 Show help for this command.
    #                             U2:\t:submit <some_text>
    #                                 Send a feedback to this bot's developer. <some_text> is the message to send.
    #                         """
    #                         )
    #                         )
}


# def execute(cmd, **kwargs):
#     """
#     Executes the callback function for the given `cmd`.
#     """
#     cmd_obj = cmds.get(cmd, None)

#     if cmd_obj is not None:
#         return cmd_obj.callback(**kwargs)