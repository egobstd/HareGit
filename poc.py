#!/usr/bin/env python

import os
import subprocess
import argparse
from datetime import datetime


def run(date):
    env = os.environ.copy()
    datestring = date.strftime(r'%Y-%m-%dT%H:%M:%S')
    env["GIT_COMMITTER_DATE"] = datestring
    env["GIT_AUTHOR_DATE"] = datestring
    subprocess.call("git commit", env=env, shell=True)


if __name__ == '__main__':
    now = datetime.today()
    parser = argparse.ArgumentParser(description='Commit at a different date and time.')
    parser.add_argument('-y', '--year', type=int, default=now.year)
    parser.add_argument('-m', '--month', type=int, default=now.month)
    parser.add_argument('-d', '--day', type=int, default=now.day)
    parser.add_argument('-j', '--hour', type=int, default=now.hour)
    parser.add_argument('-i', '--minute', type=int, default=now.minute)
    parser.add_argument('-s', '--second', type=int, default=now.second)
    args = parser.parse_args()

    fakedt = datetime(**args.__dict__)
    print "Fake date: %s" % fakedt

    run(fakedt)
