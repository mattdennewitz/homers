# Home Runs

This is a Flask app that links to every home run hit. It comes with a few commands
for importing home run data.

This app was a lazy Saturday project, and is in no way affiliated with or endorsed by MLB.

## Running this app

### Installing requirements

This app's requirements can be installed via `pip`:

```bash
$ pip install -r requirements.txt
```

### Running the web server

Running the Flask development server is as simple as:

```bash
$ python tasks.py run
```

### Importing data from MLB

```bash
$ python tasks.py import_games
```

## Data sources

Below are examples of the data sources used:

- Play-by-play data: http://gd2.mlb.com/components/game/mlb/year_2014/month_05/day_24/gid_2014_05_24_oakmlb_tormlb_1/inning/inning_all.xml
- Highlight data: http://gd2.mlb.com/components/game/mlb/year_2014/month_05/day_24/gid_2014_05_24_oakmlb_tormlb_1/media/highlights.xml
- Player data: http://gd2.mlb.com/components/game/mlb/year_2014/month_05/day_24/gid_2014_05_24_oakmlb_tormlb_1/players.xml

### Linking pbp and media data

Data is linked by reading game descriptions and media manifests,
and joining by the shared field, `sv_id`.

- `sv_id` in pbp data: `game/inning/[top/bottom]/atbat/pitch[sv_id]`
- `sv_id` in media list: `highlights/media/keywords/keyword[sv_id]`
