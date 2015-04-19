import urlparse
import datetime
import math

from flask import (Response, abort, json, redirect, render_template,
                   request, url_for)

from werkzeug.contrib.atom import AtomFeed

from homers import app, db
from homers.http import JsonResponse
from homers.models import Play, PlayView
from homers.serializers import serialize_play


@app.route('/')
def index():
    """Displays list of homers"""

    return render_template('index.html')


@app.route('/view/<int:content_id>')
def view_play(content_id):
    """Record a visit and redirect"""

    play = Play.query.filter_by(content_id=content_id).first_or_404()

    # record the hit
    pv = PlayView.query.get(content_id)
    if pv is None:
        pv = PlayView(play_id=content_id, ct=1)
        db.session.add(pv)
    else:
        pv.ct += 1

    db.session.commit()

    return redirect(play.mlbam_url())


@app.route('/homers.atom')
def feed():
    """Returns 50 latest plays"""

    feed = AtomFeed('Home Runs Only',
                    feed_url=request.url,
                    url=request.url_root)

    plays = Play.query.order_by(Play.at.desc()).limit(50)

    for play in plays:
        feed.add(play.catchy_journalist_title(),
                 'Home run hit by {batter} off of {pitcher} on {date}'.format(
                     batter=play.batter.get_full_name(),
                     pitcher=play.pitcher.get_full_name(),
                     date=play.at.strftime('%B %d, %Y'),
                 ),
                 content_type='html',
                 author=play.pitcher.get_full_name(),
                 url=urlparse.urljoin(
                     request.url_root,
                     url_for('view_play', content_id=play.content_id)),
                 updated=play.at,
                 published=play.at)

    return feed.get_response()


#
# Api v1 views
#

@app.route('/api/v1/plays')
def plays():
    """Returns paginated list of home runs.

    Note: this is also a shining example of why API frameworks
    are fantastic inventions.
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


@app.route('/api/v1/plays/date')
def plays_for_date_range():
    """Returns a list of all home runs for a certain date.
    """

    if not 'for' in request.args:
        for_date = datetime.date.today()
    else:
        try:
            for_date = datetime.datetime.strptime(request.args['for'],
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

    data = [serialize_play(play) for play in plays]

    return JsonResponse(data)
