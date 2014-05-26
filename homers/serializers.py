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
            'url': play.mlbam_url(),
        'at': play.at.isoformat(),
    }
