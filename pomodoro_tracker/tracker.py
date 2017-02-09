#!/usr/bin/env python

import click
import datetime
from tinydb import TinyDB

from .config import DB_LOCATION


@click.command()
@click.option('--db-path', default=DB_LOCATION,
              help='Db file to use.\n(default to "{}"'.format(DB_LOCATION))
@click.argument('state')
@click.argument('duration')
@click.argument('elapsed')
@click.argument('triggers', nargs=-1)
def main(db_path, state, duration, elapsed, triggers):
    db = TinyDB(db_path)
    db.insert({
        'state': state,
        'duration': duration,
        'elapsed': elapsed,
        'triggers': triggers,
        'timestamp': str(datetime.datetime.now()),
    })
    db.close()


if __name__ == "__main__":
    main()
