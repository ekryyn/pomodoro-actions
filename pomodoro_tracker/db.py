#!/usr/bin/env python

import click
import datetime
from .config import DB_LOCATION
from tinydb import TinyDB, Query
import csv

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


def _summary(db, start=None, end=None):
    """
    Get a summary of pomodoros for a given date range.

    :param db: TinyDB connection
    :param start: if given, only consider records from `start`
    :type start: `datetime.datetime`
    :param end: if given, only consider records until `end`
    :type end: `datetime.datetime`
    """
    q = Query()

    start = start or datetime.datetime(1970, 1, 1)
    end = end or datetime.datetime.now()

    start = str(start)
    end = str(end)

    date_range = (q.timestamp >= start) & (q.timestamp < end)

    complete = db.count((q.state == 'pomodoro') &
                        (q.triggers.any(['complete'])) &
                        date_range)
    started = db.count((q.state == 'pomodoro') &
                       (q.triggers.any(['start'])) &
                       date_range)
    ratio = 0 if not started else complete/float(started) * 100
    return {
        'complete': complete,
        'started': started,
        'ratio': ratio,
    }


def summary_print(complete, started, ratio):
    print("Pomodoro summary :")
    print("  Complete pomodoros: {}".format(complete))
    print("  Started pomodoros: {}".format(started))
    print("  Ratio: {}%".format(ratio))


@click.group()
@click.option('--db-path', default=DB_LOCATION,
              help='Db file to use.\n(default to "{}"'.format(DB_LOCATION))
@click.pass_context
def main(ctx, db_path):
    ctx.obj = {'db_path': db_path}


@main.command()
@click.pass_context
def summary(ctx):
    db = TinyDB(ctx.obj['db_path'])
    s = _summary(db)
    summary_print(**s)
    db.close()


@main.command()
@click.pass_context
def day_summary(ctx):
    db = TinyDB(ctx.obj['db_path'])
    st = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    en = st + datetime.timedelta(days=1)
    s = _summary(db, st, en)
    summary_print(**s)
    db.close()


@main.command()
@click.pass_context
def dump(ctx):
    db = TinyDB(ctx.obj['db_path'])
    data = db.all()
    out = StringIO()
    headers = ['timestamp', 'state', 'duration', 'elapsed', 'triggers']
    w = csv.DictWriter(out, fieldnames=headers)
    w.writeheader()
    for row in data:
        row['triggers'] = ' '.join(row['triggers'])
        w.writerow(row)
    db.close()
    out.seek(0)
    print(out.read())


if __name__ == "__main__":
    main()
