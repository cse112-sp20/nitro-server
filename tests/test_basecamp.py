from basecamp import *


def test_parse_points():
    s = "some long line of text like this (255)"
    ss = "some long line of text like this (0)"
    assert parse_points(s) == 255
    assert parse_points(ss) == 0

def test_get_points_available():
    li = [
        {'points': 10},
        {'points': 20},
        {'points': 30},
        {'points': 40}
    ]
    assert get_points_available(li) == 100
