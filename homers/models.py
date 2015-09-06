from __future__ import unicode_literals

import datetime

import dateutil.parser

from homers import db
from homers.desc import phrase_ring


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
    """Represents a play, who was involved, and the time
    """
    __tablename__ = 'plays'

    content_id = db.Column(db.Integer, primary_key=True)
    batter_id = db.Column(db.Integer, db.ForeignKey('players.mlbam_id'))
    pitcher_id = db.Column(db.Integer, db.ForeignKey('players.mlbam_id'))
    batter_team = db.Column(db.String(3))
    pitcher_team = db.Column(db.String(3))
    play_type = db.Column(db.Text)
    at = db.Column(db.DateTime)
    sv_id = db.Column(db.String(24))
    runs_on_play = db.Column(db.Integer())
    video_url = db.Column(db.Text)

    # media-specific info
    headline = db.Column(db.Text)
    blurb = db.Column(db.Text)

    batter = db.relationship('Player', foreign_keys=batter_id)
    pitcher = db.relationship('Player', foreign_keys=pitcher_id)

    def __init__(self, batter_id, pitcher_id,
                 batter_team, pitcher_team,
                 play_type, at, sv_id, runs_on_play,
                 content_id, headline, blurb,
                 video_url):
        self.batter_id = batter_id
        self.batter_team = batter_team
        self.pitcher_id = pitcher_id
        self.pitcher_team = pitcher_team
        self.play_type = play_type
        self.sv_id = sv_id
        self.video_url = video_url
        self.runs_on_play = runs_on_play
        self.content_id = content_id
        self.headline = headline
        self.blurb = blurb

        if isinstance(at, datetime.datetime):
            self.at = at
        elif isinstance(at, basestring) and at.endswith('Z'):
            self.at = dateutil.parser.parse(at)

    def __repr__(self):
        return '%s v. %s' % (self.batter.get_full_name(),
                             self.pitcher.get_full_name())

    def mlbam_url(self):
        return ('http://mlb.mlb.com/video/play.jsp?content_id=%s' %
                self.content_id)
