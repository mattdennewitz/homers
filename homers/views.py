import urlparse
import datetime
import math

from flask import (Response, abort, json, redirect, render_template,
                   request, url_for)

from sqlalchemy.sql.expression import func

from werkzeug.contrib.atom import AtomFeed

from homers import app, db
from homers.http import JsonResponse
from homers.models import Play
from homers.serializers import serialize_play


@app.route('/homers.atom')
def feed():
    """Returns 50 latest plays"""

    feed = AtomFeed('Home Runs Only',
                    feed_url=request.url,
                    url=request.url_root)

    plays = Play.query.order_by(Play.at.desc()).limit(50)

    for play in plays:
        feed.add(title=play.blurb,
                 content_type='html',
                 author=play.pitcher.get_full_name(),
                 url=play.video_url,
                 updated=play.at,
                 published=play.at,
                 id=play.content_id)

    return feed.get_response()


#
# Api v1 views
#

@app.route('/api/v1/randomdinger')
def random_dinger():
    """Returns a random home run
    """

    play = Play.query.order_by(func.random()).first()

    return JsonResponse(serialize_play(play))


@app.route('/api/v1/plays')
def plays():
    """Returns paginated list of home runs.
    """

    try:
        page_number = int(request.args.get('page', 1))
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    total_ct = Play.query.count()
    page_ct = int(math.ceil(float(total_ct) / app.config['PER_PAGE']))

    if page_number > page_ct:
        abort(404)

    offset = (page_number - 1) * app.config['PER_PAGE']
    limit = offset + app.config['PER_PAGE']
    plays = Play.query.order_by(Play.at.desc()).slice(offset, limit)

    if (page_number + 1) >= page_ct:
        next_page_number = None
    else:
        next_page_number = page_number + 1

    resp = {
        'meta': {
            'total': total_ct,
            'pages': page_ct,
            'next_page_number': next_page_number,
        },
        'plays': [serialize_play(play) for play in plays]
    }

    return JsonResponse(resp)
