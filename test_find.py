import pytest
import find

class Args():
    def __init__(self, root, name):
        self.root = root
        self.name = name


@pytest.fixture
def args():
    return Args(['./sample-files'], ['rw*'])


def test_find(args):
    print(args.name)
    matches = find.find(args)

    shouldbe = [['./sample-files/rw'],
    ['./sample-files/rw50-1M.json'],
    ['./sample-files/rw50-8k.json'],
    ['./sample-files/rw70-1M.json'],
    ['./sample-files/rw70-8k.json'],
    ['./sample-files/rw/rw50-1M.json'],
    ['./sample-files/rw/rw8k.json']]

    assert len(matches) == len(shouldbe)

    for i in range(len(matches)):
        assert matches[i] == shouldbe[i][0]
