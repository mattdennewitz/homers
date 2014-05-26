from __future__ import unicode_literals

import datetime

import dateutil.parser

from homers import db


class Player(db.Model):
    """Represents a single player"""
    __tablename__ = 'players'

    mlbam_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def __init__(self, mlbam_id, first_name, last_name):
        self.mlbam_id = mlbam_id
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
    batter_team = db.Column(db.String(3))
    pitcher_team = db.Column(db.String(3))
    play_type = db.Column(db.Text)
    at = db.Column(db.DateTime)
    sv_id = db.Column(db.String(24))

    # media-specific info
    headline = db.Column(db.Text)
    blurb = db.Column(db.Text)

    batter = db.relationship('Player', foreign_keys=batter_id)
    pitcher = db.relationship('Player', foreign_keys=pitcher_id)

    def __init__(self, batter_id, pitcher_id,
                 batter_team, pitcher_team,
                 play_type, at, sv_id,
                 content_id, headline, blurb):
        self.batter_id = batter_id
        self.batter_team = batter_team
        self.pitcher_id = pitcher_id
        self.pitcher_team = pitcher_team
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


class PlayView(db.Model):
    __tablename__ = 'play_views'

    play_id = db.Column(db.Integer, db.ForeignKey('plays.content_id'),
                        unique=True, primary_key=True)
    ct = db.Column(db.Integer)

    play = db.relationship('Play', foreign_keys=play_id)

    def __repr__(self):
        return '%s - %s view(s)' % (self.play.content_id, self.ct)
