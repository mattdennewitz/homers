import hash_ring

__all__ = ('phrase_ring', )


phrases = (
    '%(batter)s homers off of %(pitcher)s',
    '%(batter)s destroys a pitch from %(pitcher)s',
    '%(batter)s puts one out off of %(pitcher)s',
    '%(batter)s makes a souvenir out of one from %(pitcher)s',
    '%(batter)s takes %(pitcher)s deep',
    '%(batter)s goes deep off %(pitcher)s',
    '%(batter)s crushes one from %(pitcher)s',
    '%(batter)s hits a dinger off of %(pitcher)s',
    "%(batter)s touches 'em all against %(pitcher)s",
    '%(batter)s hits a gopher ball off of %(pitcher)s',
    '%(batter)s goes yard off of %(pitcher)s',
)

phrase_ring = hash_ring.HashRing(phrases)

