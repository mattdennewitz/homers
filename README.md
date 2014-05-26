# Home Runs

This is a Flask app that links to every home run hit. It comes with a few commands
for importing home run data.

This app was a lazy Saturday project, and is in no way affiliated with or endorsed by MLB.

## Running this app

First, fork and clone this repo.

### Installing requirements

This app's requirements can be installed via `pip`:

```bash
$ pip install -r requirements.txt
```

### Set up the database

This app was written for and testing using Postgres,
but should be compatible with other database platforms
through SQLAlchemy.

Create a database, and then

1. Update `SQLALCHEMY_DATABASE_URI` in either `homers.config`
   or `homers.local_config`. Alternately, this app will read
   `DATABASE_URL` from your environment before trying the config.
2. Run the `create_db` task:

```bash
$ python tasks.py create_db
```

After these steps, you should have an empty database.

### Importing data from MLB

This app comes with the ability to import game data from MLBAM.
This importer is run through `tasks.py`:

```bash
$ python tasks.py import_games
```

Games can be imported one of two ways: by day and by year.

#### Games by day

To import games for one or more dates, provide one or more `-d` arguments
to `import_games`. Dates given should be given as `YYYY-MM-DD`.

```bash
$ python tasks.py import_games -d 2014-05-01 -d 2014-04-01
```

#### Games by year

To import games for an entire year, use the `-y` flag:

```bash
$ python tasks.py import_games -y 2014
```

Imports are powered by [mlbma-utils](github.com/mattdennewitz/mlbam-utils).

### Running the web server

Running the Flask development server is as simple as:

```bash
$ python tasks.py run
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
