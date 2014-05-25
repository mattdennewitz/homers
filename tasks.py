import datetime

from homers import app, db, tasks

import click


@click.group()
def cli(): pass


@cli.command()
def create_db():
    """Creates database"""
    db.create_all()


@cli.command()
@click.option('for_date', '-d', required=False)
@click.option('download', '--skip-download/--download', default=False)
def import_games(for_date, download):
    """Imports games for today"""

    if for_date is None:
        for_date = datetime.date.today()
    else:
        for_date = datetime.date(
            *datetime.datetime.strptime(for_date, '%Y-%m-%d').timetuple()[:3])

    tasks.import_plays_by_date(for_date, download)


@cli.command()
def run():
    app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    cli()
