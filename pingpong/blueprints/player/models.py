import datetime
from collections import OrderedDict
from hashlib import md5
import pytz
from flask_login import UserMixin


class Player(UserMixin):
    """
        Store all registered players in a  static list.
        This simulates sqlalchemy behavior if we needed a DB.
    """
    Db = []
    
    def __init__(self, uid, username, password, defense, **kwargs):
        # Call  constructor.
        super(Player, self).__init__(**kwargs)
        self.uid = uid
        self.username = username
        self.defense = defense
        self.password = password
        Player.Db.append(self)

    @classmethod
    def find_by_username(cls, username):
        """
        Find a player by username.

        :param identity: username
        :type identity: str
        :return: Player instance
        """
        for player in Player.Db:
            if player.username == username:
                return player
        return None

    @classmethod
    def find_by_uid(cls, uid):
        """
        Find a player by uid.

        :param identity: uid
        :type identity: int
        :return: Player instance
        """
        for player in Player.Db:
            if player.uid == int(uid):
                return player
        return None


    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return True

    def authenticated(self, password):
        """
        Authenticate by checking their password.

        :param password:  password for the user
        :type password: str
        :return: bool
        """
        return self.password == password

    def get_id(self):
        """
        Overrides flask_login get_id method

        :return: int
        """
        return self.uid