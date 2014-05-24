import datetime

from flask import Response, json, render_template, request
from flask.ext.restful import Resource

from homers import app
from homers.models import Play


@app.route('/')
def index():
    """Displays list of homers"""

    return render_template('index.html')


#
# Api v1 views
#

@app.route('/api/v1/plays')
def plays_for_date_range():
    if not 'start_date' in request.args:
        max_date = datetime.date.today()
    else:
        try:
            max_date = datetime.datetime.strptime(request.args['max_date'],
                                                    '%Y-%m-%d')
            max_date = datetime.date(*max_date.timetuple()[:3])
        except ValueError:
            return Response(json.dumps({'error': 'Provide start date as Y-m-d'}),
                            status=400, content_type='application/json')

    min_date = max_date - datetime.timedelta(days=app.config['DAYS_PER_PAGE'])

    plays = (Play.query
             .filter(Play.at.between(
                 min_date.strftime('%Y-%m-%d 00:00:00'),
                 max_date.strftime('%Y-%m-%d 23:59:59')
             ))
             .order_by(Play.at.desc()))

    data = [
        {
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
            'at': play.at,
        }
        for play in plays
    ]

    return Response(json.dumps(data),
                    status=200,
                    content_type='application/json')
