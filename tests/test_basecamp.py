from Basecamp import *
import Database_Access_Object
import json

def test_parse_points():
    bc = Basecamp("dummy", "data")
    # not really sure how the regex works
    # title = ""
    # point = bc.parse_points(title)
    # assert point == 400