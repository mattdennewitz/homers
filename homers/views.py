import calendar
import datetime
import itertools

import pytz

from flask import Response, json, render_template, request

from homers import app
from homers.models import Play


@app.route('/')
def index():
    """Displays list of homers"""

    return render_template('index.html')


#
# Api v1 views
#

et_tz = pytz.timezone('America/New_York')

@app.route('/api/v1/plays')
def plays_for_date_range():
    if not 'for_date' in request.args:
        for_date = datetime.date.today()
    else:
        try:
            for_date = datetime.datetime.strptime(request.args['for_date'],
                                                    '%Y-%m-%d')
            for_date = datetime.date(*for_date.timetuple()[:3])
        except ValueError:
            return Response(json.dumps({'error': 'Provide start date as Y-m-d'}),
                            status=400, content_type='application/json')

    plays = (Play.query
             .filter(Play.at.between(
                 for_date.strftime('%Y-%m-%d 00:00:00'),
                 for_date.strftime('%Y-%m-%d 23:59:59')
             ))
             .order_by(Play.at.desc()))

    data = []

    for play in plays:
        desc = {
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
            'url': play.mlbam_url(),
            'at': play.at.isoformat(),
        }
        data.append(desc)

    return Response(json.dumps(data),
                    status=200,
                    content_type='application/json')
