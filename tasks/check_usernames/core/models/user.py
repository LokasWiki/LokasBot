class UserStatus:
    STATE_GET_FROM_DB = 0
    STATE_SEND_TO_API = 1
    STATE_ACCEPT_ON_API = 2
    STATE_REJECT_ON_API = 3


class User:

    def __init__(self, id, user_name, created_at, status=UserStatus.STATE_GET_FROM_DB):
        self.id = id
        self.user_name = user_name
        self.created_at = created_at
        self.status = status
