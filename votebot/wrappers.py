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