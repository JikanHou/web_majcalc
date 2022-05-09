import datetime

from flask_login import UserMixin
from majcalc import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
game_player_ass_table = db.Table('association', db.Column('userID', db.Integer, db.ForeignKey('user.id')), db.Column('gameID', db.Integer, db.ForeignKey('game.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(40), unique = True)
    passwordHash = db.Column(db.String(128))
    avatar = db.Column(db.String(128), default = "defaultAvatar.png")
    note = db.Column(db.String(128), default = "这个人没有留下签名")
    rank = db.Column(db.Integer, default = 1)
    pt = db.Column(db.Integer, default = 0)
    uploadGames = db.relationship('Game', back_populates = 'uploader')
    games = db.relationship('Game', secondary = game_player_ass_table, back_populates = 'players')

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def validatePassword(self, password):
        return check_password_hash(self.passwordHash, password)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    uploader = db.relationship('User', back_populates = 'uploadGames')
    rounds = db.relationship('Round', back_populates = 'game', cascade = 'all, delete-orphan')
    players = db.relationship('User', secondary = game_player_ass_table, back_populates = 'games')
    start_time = db.Column(db.DateTime, default = datetime.datetime.now())
    results = db.relationship('Result', back_populates = 'game', cascade = 'all, delete-orphan')


class Round(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    game = db.relationship('Game', back_populates = 'rounds')
    round = db.Column(db.Integer)
    bonba = db.Column(db.Integer, default = 0)
    result = db.Column(db.String(128), default = "25000 25000 25000 25000 0") # E S W N 供托 split by $
    reason = db.Column(db.String(256))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    game = db.relationship('Game', back_populates = "results")
    player_id = db.Column(db.Integer)
    player_nickname = db.Column(db.String(128))
    player_point = db.Column(db.Integer)
