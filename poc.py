#!/usr/bin/env python

import os
import subprocess
import argparse
from datetime import datetime


def makeenv(date):
    datestring = date.strftime(r'%Y-%m-%dT%H:%M:%S')
    return {'GIT_COMMITTER_DATE': datestring, 'GIT_AUTHOR_DATE': datestring}


def commit(date):
    env = os.environ.copy()
    env.update(makeenv(date))
    subprocess.check_call(["/usr/bin/env", "git", "commit"], env=env)


def get_last_commit_datetime(author=None):
    args = ["/usr/bin/env", "git", "log",
            "--color=never", "--pretty=%at", "--date=local", "-F",
            "--all", "--max-count=1", "--date-order"]
    if author:
        args.append("--author=%s" % author)
    output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    timestamp = int(output.strip())

    return datetime.fromtimestamp(timestamp)


if __name__ == '__main__':
    now = datetime.today()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_commit = subparsers.add_parser('fakedate',
            help='Commit at a different date and time.')
    parser_commit.add_argument('-y', '--year', type=int, default=now.year)
    parser_commit.add_argument('-m', '--month', type=int, default=now.month)
    parser_commit.add_argument('-d', '--day', type=int, default=now.day)
    parser_commit.add_argument('-j', '--hour', type=int, default=now.hour)
    parser_commit.add_argument('-i', '--minute', type=int, default=now.minute)
    parser_commit.add_argument('-s', '--second', type=int, default=now.second)
    parser_commit.add_argument('-a', '--action', default="commit")
    parser_lastcommit = subparsers.add_parser('lastcommit',
            help='Get the last commit date and time.')
    parser_lastcommit.set_defaults(action="lastcommit")
    args = parser.parse_args()
    action = args.action

    if action == "commit" or action == "getenv":
        fakedt = datetime(year=args.year, month=args.month, day=args.day,
                        hour=args.hour, minute=args.minute, second=args.second)
        print "Fake date: %s" % fakedt
        if action == "commit":
            commit(fakedt)
        if action == "getenv":
            print ' '.join(['%s="%s"' % (k, v) for k, v in makeenv(fakedt).iteritems()])
    elif action == "lastcommit":
        print "Last commit at: %s" % get_last_commit_datetime()
