import datetime
import glob
import os

from lxml import etree

from mlbam_utils.download import find_games_for_date, download_data

from homers import app, db
from homers.exceptions import PlayerNotFound
from homers.models import Player, Play


def get_player(doc, player_id):
    """Get or create a player using an MLBAM player list node
    """

    try:
        player_data = doc.xpath('//player[@id=%s]' % player_id)[0]
    except IndexError:
        raise PlayerNotFound('Player %s not found in given player list.' %
                             player_id)

    player = Player.query.get(player_data.get('id'))

    if player is None:
        player = Player(mlbam_id=player_data.get('id'),
                        first_name=player_data.get('first'),
                        last_name=player_data.get('last'))
        db.session.add(player)
        db.session.commit()

    return (player, player_data.get('team_abbrev'))


def import_plays_by_date(for_date=None):
    """Imports and saves games for date"""

    if for_date is None:
        for_date = datetime.date.today()

    target_files = {
        'innings': 'inning/inning_all.xml',
        'highlights': 'media/highlights.xml',
        'players': 'players.xml'
    }

    # download player info, play-by-play, and media list
    # download_data([for_date], app.config['DATA_DIR'], target_files.values())

    path_f = os.path.join(app.config['DATA_DIR'],
                          '*%s_%02d_%02d*' % (for_date.year,
                                              for_date.month,
                                              for_date.day))
    game_paths = glob.glob(path_f)

    for path in game_paths:
        data = {
            key: etree.fromstring( open(os.path.join(path, value)).read() )
            for key, value
            in target_files.items()
            if os.path.exists(os.path.join(path, value))
        }

        # reject games without complete descriptions
        if len(data) < 3:
            continue

        # search through play-by-play events to find home runs,
        # and pair with gameday video (if available)
        hr_atbats = data['innings'].xpath('//atbat[@event="Home Run"]')

        if len(hr_atbats) == 0:
            continue

        for atbat in hr_atbats:
            # get last pitch's sv_id, the key on which
            # we'll join highlights and pbp data
            sv_id = atbat.xpath('./pitch')[-1].get('sv_id')

            # locate record in highlights reel
            try:
                highlights = data['highlights'].xpath(
                    '//keyword[@type="sv_id" and @value="%s"]/../..' % sv_id)
                highlight = highlights[0]
            except IndexError:
                # no highlight for this play
                print 'No highlight found for %s' % sv_id
                continue

            content_id = highlight.get('id')

            # have we seen this play?
            if Play.query.filter_by(content_id=content_id).count() > 0:
                print 'Play %s already logged. Skipping.' % content_id
                continue

            # create participants, play
            batter, b_team = get_player(data['players'], atbat.get('batter'))
            pitcher, p_team = get_player(data['players'], atbat.get('pitcher'))

            play = Play(content_id = content_id,
                        batter_id = batter.mlbam_id,
                        pitcher_id = pitcher.mlbam_id,
                        batter_team = b_team,
                        pitcher_team = p_team,
                        play_type = 'Home Run',
                        at = atbat.get('start_tfs_zulu'),
                        sv_id = sv_id,
                        headline = highlight.get('headline'),
                        blurb = highlight.get('blurb'))

            db.session.add(play)
            db.session.commit()
