import flask
import free_times
import flask_main
import nose
from free_times import list_freeblocks, freetimes

#tests for freetimes(freeblock, busytimes) in free_times.py


def test_no_free_time():
	#if there's no free times
	free_time = []
	busy_time = [{'start': '2017-02-02T10:00:00-8:00', 'end': '2017-02-02T15:00:00-08:00', 'sum': 'test event'}]
	result = freetimes(free_time, busy_time)
	assert result == []

def test_no_busy_time():
	#if there's no busy times
	free_time = {'start': '2017-02-02T10:00:00-8:00', 'end': '2017-02-02T15:00:00-08:00', 'sum': 'test event'}
	busy_time = []
	result = freetimes(free_time, busy_time)
	assert len(result) == 1

#tests for list_freeblocks

def test_empty_block():
	#list_freeblocks makes an empty time slot for the selected range each day,
	#so what if the time range doesn't allow this?

	start = "2015-01-01T00:00:00+00:00"
	end = "2014-01-01T00:00:00+00:00"
	result = list_freeblocks(start, end)
	assert result == []

def test_single_dayblock():
	#if only one day is selected for the date range, there should only be one freeblock created
	#in the list of freeblocks that list_freeblocks returns
	start = "2015-01-01T01:00:00+00:00"
	end = "2015-01-01T20:00:00+00:00"
	result = list_freeblocks(start, end)
	assert len(result) == 1

def test_multiple_dayblocks():
	#if the range consists of multiple days, the length of the list returned by list_freeblocks
	#should match how many days are in the range.
	start = "2013-05-01T03:00:00+00:00"
	end = "2013-05-07T18:00:00+00:00"
	result = list_freeblocks(start, end)
	assert len(result) == 7








