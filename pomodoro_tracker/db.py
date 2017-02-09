#!/usr/bin/env python

import click
from .config import DB_LOCATION
from tinydb import TinyDB, Query
import csv

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


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

    q = Query()
    pom_complete = db.count((q.state == 'pomodoro') &
                            (q.triggers.any(['complete'])))
    pom_started = db.count((q.state == 'pomodoro') &
                            (q.triggers.any(['start'])))
    ratio = 0 if not pom_started else pom_complete/float(pom_started) * 100
    print("Pomodoro summary :")
    print("  Complete pomodoros: {}".format(pom_complete))
    print("  Started pomodoros: {}".format(pom_started))
    print("  Ratio: {}%".format(ratio))
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
