import sqlite3
import argparse
import sys
from datetime import date


def parseArgs():
    parser = argparse.ArgumentParser(description='Save and retrieve todo items')
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('--date', nargs='?')
    parser_add.add_argument('--tags', nargs='?')
    parser_add.add_argument('task', nargs='+')


    parser_search = subparsers.add_parser('search')
    parser_search.add_argument("--from", nargs=1, dest = 'from_')
    parser_search.add_argument("--to", nargs=1)
    parser_search.add_argument("--today", action='store_true')
    parser_search.add_argument("--tag", nargs='?')
    parser_search.add_argument('task', nargs='*')

    parser_done = subparsers.add_parser('done')
    parser_done.add_argument("--tag", nargs='?')
    parser_done.add_argument('task', nargs='*')

    return parser.parse_args()


def genDB():
    db = sqlite3.connect("./proj4.db")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todos (task varchar(200), tags varchar(500), dt date, done INTEGER)")
    return db


def printMatches(matches, printDate=True, printTags=True):
    for match in matches:
        desc = match[0] if match[0] else ""
        tags = match[1] if match[1] else ""
        date = match[2] if match[2] else ""

        print(desc + "  ", end='')

        if printTags:
            print("tags:" + tags + " ", end='')

        if printDate:
            print("date:" + date, end='')

        print()


def processAdd(db, args):
    cur = db.cursor()
    dt = date.fromisoformat(args.date)
    tk = ' '.join(args.task)
    cur.execute("INSERT INTO todos (task, tags, dt, done) VALUES (?, ?, ?, FALSE);", [tk, args.tags, dt])
    db.commit()


def processSearch(db, args):
    cur = db.cursor()

    if args.today:
        today = str(date.today())
        cur.execute("SELECT * FROM todos WHERE dt = ?;", [today])
        printMatches(cur.fetchall())
    elif args.from_ and args.to:
        fr = args.from_[0]
        to = args.to[0]
        cur.execute("SELECT * FROM todos WHERE dt BETWEEN (?) AND (?);", [fr, to]);
        printMatches(cur.fetchall(), printDate=False)
    elif args.task or args.tag:
        tag = args.tag if args.tag else ""
        cur.execute("SELECT * FROM todos WHERE task LIKE (?) AND tags LIKE (?);", ["%" + ' '.join(args.task) + "%", "%" + tag + "%"])
        printMatches(cur.fetchall(), printDate=False, printTags=False)


def processDone(db, args):
    cur = db.cursor()

    if args.task or args.tag:
        tag = args.tag if args.tag else ""
        print(tag)
        cur.execute("UPDATE todos SET done=TRUE WHERE task LIKE (?) AND tags LIKE (?);", ["%" + ' '.join(args.task) + "%", "%" + tag + "%"])
        db.commit()
    else:
        print("Error: please provide tasks or tags to mark as complete")


if __name__ == '__main__':
    args = parseArgs()
    db = genDB()

    if args.command == 'add':
        processAdd(db, args)
    elif args.command == 'search':
        processSearch(db, args)
    elif args.command == 'done':
        processDone(db, args)