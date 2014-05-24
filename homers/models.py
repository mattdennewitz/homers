from __future__ import unicode_literals

import datetime

import dateutil.parser

from homers import db


class Player(db.Model):
    """Represents a single player"""
    __tablename__ = 'players'

    mlbam_id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def __init__(self, mlbam_id, team, first_name, last_name):
        self.mlbam_id = mlbam_id
        self.team = team
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class Play(db.Model):
    """Represents a play, who was involved, and the time"""
    __tablename__ = 'plays'

    content_id = db.Column(db.Integer, primary_key=True)
    batter_id = db.Column(db.Integer, db.ForeignKey('players.mlbam_id'))
    pitcher_id = db.Column(db.Integer, db.ForeignKey('players.mlbam_id'))
    play_type = db.Column(db.Text)
    at = db.Column(db.DateTime)
    sv_id = db.Column(db.String(24))

    # media-specific info
    headline = db.Column(db.Text)
    blurb = db.Column(db.Text)

    # batter = db.relationship(
    #     Player, backref=db.backref('hits', lazy='dynamic'))
    # pitcher = db.relationship(
    #     Player, backref=db.backref('pitches', lazy='dynamic'))

    # batter = db.relationship(Player, foreign_keys=[Play.batter_id],
    #                          backref=db.backref('hits', lazy='dynamic'))
    # pitcher = db.relationship(Player, foreign_keys=[Play.pitcher_id],
    #                          backref=db.backref('hits', lazy='dynamic'))

    def __init__(self, batter_id, pitcher_id, play_type, at, sv_id,
                 content_id, headline, blurb):
        self.batter_id = batter_id
        self.pitcher_id = pitcher_id
        self.play_type = play_type
        self.sv_id = sv_id
        self.content_id = content_id
        self.headline = headline
        self.blurb = blurb

        if isinstance(at, datetime.datetime):
            self.at = at
        elif isinstance(at, basestring) and at.endswith('Z'):
            self.at = dateutil.parser.parse(at)

    def mlbam_url(self):
        return ('http://mlb.mlb.com/video/play.jsp?content_id=%s' %
                self.content_id)
