import pytest
import proj4
import os
from datetime import date


class ArgsAdd():
    def __init__(self, date, tags, task ):
        self.date = date
        self.tags = tags
        self.task = task


class ArgsSearch():
    def __init__(self, from_, to, today, tag, task):
        self.from_ = from_
        self.to = to
        self.today = today 
        self.tag = tag
        self.task = task


class ArgDone():
    def __init__(self, tag, task):
        self.tag = tag
        self.task = task


def test_add():
    dbname = "./proj4Test.db"
    db = proj4.genDB(dbname)
    args = ArgsAdd('2022-02-01', 'room,home,chore', ['Clean my room'])
    proj4.processAdd(db, args)
    args = ArgsAdd('2021-01-27', 'kitchen,home,chore', ['Wash the dishes'])
    proj4.processAdd(db, args)

    cur = db.cursor()
    x = cur.execute("SELECT * FROM todos").fetchall()
    os.remove(dbname)

    mustbe = [('Clean my room', 'room,home,chore', '2022-02-01', 0), 
    ('Wash the dishes', 'kitchen,home,chore', '2021-01-27', 0)]

    assert x == mustbe


def test_search():
    dbname = "./proj4Test.db"
    db = proj4.genDB(dbname)
    args = ArgsAdd('2022-02-01', 'room,home,chore', ['Clean my room'], )
    proj4.processAdd(db, args)
    args = ArgsAdd(date.today().strftime("%Y-%m-%d"), 'kitchen,home,chore', ['Wash the dishes'], )
    proj4.processAdd(db, args)

    args = ArgsSearch(None, None, True, None, None)
    x = proj4.processSearch(db, args)
    print(x)
    assert x == [('Wash the dishes', 'kitchen,home,chore', date.today().strftime("%Y-%m-%d"), 0)]

    args = ArgsSearch(['2021-12-31'], ['2022-13-31'], None, None, None)
    x = proj4.processSearch(db, args)
    assert x == [('Clean my room', 'room,home,chore', '2022-02-01', 0), ('Wash the dishes', 'kitchen,home,chore', date.today().strftime("%Y-%m-%d"), 0)]

    args = ArgsSearch(None, None, None, 'home', [])
    x = proj4.processSearch(db, args)
    assert x == [('Clean my room', 'room,home,chore', '2022-02-01', 0), ('Wash the dishes', 'kitchen,home,chore', date.today().strftime("%Y-%m-%d"), 0)]

    args = ArgsSearch(None, None, None, 'home', ['Wash'])
    x = proj4.processSearch(db, args)
    assert x == [('Wash the dishes', 'kitchen,home,chore', date.today().strftime("%Y-%m-%d"), 0)]

    os.remove(dbname)


def test_done():
    dbname = "./proj4Test.db"
    db = proj4.genDB(dbname)
    args = ArgsAdd('2022-02-01', 'room,home,chore', ['Clean my room'], )
    proj4.processAdd(db, args)
    args = ArgsAdd(date.today().strftime("%Y-%m-%d"), 'kitchen,home,chore', ['Wash the dishes'], )
    proj4.processAdd(db, args)

    args = ArgDone('', ['Clean my room']);
    x = proj4.processDone(db, args)
    assert x == [('Clean my room', 'room,home,chore', '2022-02-01', 0)]

    args = ArgDone('home', []);
    x = proj4.processDone(db, args)
    assert x == [('Clean my room', 'room,home,chore', '2022-02-01', 1), ('Wash the dishes', 'kitchen,home,chore', '2022-01-28', 0)]

    cur = db.cursor()
    x = cur.execute("SELECT * FROM todos").fetchall()
    assert x == [('Clean my room', 'room,home,chore', '2022-02-01', 1), ('Wash the dishes', 'kitchen,home,chore', '2022-01-28', 1)]

    os.remove(dbname)