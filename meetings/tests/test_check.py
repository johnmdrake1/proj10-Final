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
def test_trans():
	events = [{"sum": "test event", "transparency": " ", "start":"2017-01-01T00:00:00+00:00", "end": "2017-02-01T00:00:00+00:00"}]
	start = "2017-01-01T00:00:00+00:00"
	end = "2017-02-01T00:00:00+00:00"
	result = cmps(events, start, end)
	assert result=="no events"


# 3.checking if there is event in a space where it should be

def test_event():
	events = [{"sum": "test event", "start": "2017-01-01T00:00:00+00:00", "end": "2017-03-01T11:59:00+00:00"}]
	st = "2017-01-01T00:00:00+00:00"
	et = "2017-05-05T11:59:00+00:00"
	result = cmps(events, st, et)
	#this one might not be working, remove for other tests
	assert result not empty or (result!="no events")

