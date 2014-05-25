import datetime
import multiprocessing
import os

from homers import app, db, tasks
from homers.utils import make_date, generate_year_series

import click


@click.group()
def cli(): pass


@cli.command()
def create_db():
    """Creates database"""
    db.create_all()


@cli.command()
@click.option('download', '--skip-download/--download', default=False)
@click.option('date_set', '-d', required=False, multiple=True)
@click.option('year', '-y', type=click.INT, required=False)
@click.option('workers', '-w', type=click.INT, required=False)
def import_games(download, date_set=None, year=None, workers=None):
    """Imports games for today"""

    # ensure data directory exists, creating if not
    if not os.path.exists(app.config['DATA_DIR']):
        os.mkdir(app.config['DATA_DIR'])

    if workers is None:
        workers = multiprocessing.cpu_count()

    if year:
        date_set = generate_year_series(year)
    elif date_set:
        date_set = [make_date(v) for v in date_set]
    else:
        date_set = [datetime.date.today()]

    # spread out downloads across a few processes
    pool = multiprocessing.Pool(workers)

    for date in date_set:
        pool.apply_async(tasks.import_plays_by_date, [date, download])

    pool.close()
    pool.join()


@cli.command()
def run():
    app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    cli()
