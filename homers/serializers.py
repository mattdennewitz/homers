import pytz

from flask import url_for


et_tz = pytz.timezone('America/New_York')

def serialize_play(play):
    return {
        'batter': {
            'name': play.batter.get_full_name(),
            'team': play.batter_team,
            'id': play.batter_id,
        },
            'pitcher': {
                'name': play.pitcher.get_full_name(),
                'id': play.pitcher_id,
                'team': play.pitcher_team,
            },
            'url': url_for('view_play', content_id=play.content_id),
        'at': et_tz.localize(play.at).strftime('%Y-%m-%dT%H:%M:%S%z'),
    }
