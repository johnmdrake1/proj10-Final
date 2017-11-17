import nose
import flask
from flask_main import cmp_times as cmps

# 1.empty list
def test_empty():
	events = []
	start = "2017-01-01T00:00:00+00:00"
	end = "2017-02-01T00:00:00+00:00"
	result = cmps(events, start, end)
	assert result=="no events"


# 2.transparency


# 3.checking if there is event in a space where it should be

