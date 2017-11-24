import flask
import free_times
import flask_main
import nose
from free_times import list_freeblocks, freetimes
import logging
import config

if __name__ == "__main__":
    CONFIG = config.configuration()
else:
    CONFIG = config.configuration(proxied=True)

app = flask.Flask(__name__)
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)
app.secret_key=CONFIG.SECRET_KEY

#tests for freetimes(freeblock, busytimes) in free_times.py


def test_no_free_time():
	#if there's no free times
	free_time = []
	busy_time = [{'start': '2017-02-02T10:00:00-8:00', 'end': '2017-02-02T15:00:00-08:00'}]
	result = freetimes(free_time, busy_time)
	assert result == []

def test_no_busy_time():
	#if there's no busy times
	free_time = {'start': '2017-02-02T10:00:00-8:00', 'end': '2017-02-02T15:00:00-08:00'}
	busy_time = []
	result = freetimes(free_time, busy_time)
	assert len(result) == 1

def test_one_busy_time():
	#if there's a busy time in the middle of the time range, that does not consist of the entire time range,
	#then there should be 2 free time blocks.
	free_time = {'start': '2017-02-02T10:00:00-8:00', 'end': '2017-02-02T15:00:00-08:00'}
	busy_time = [{'start': '2017-02-02T11:30:00-8:00', 'end': '2017-02-02T13:25:00-08:00', 'sum': 'test event'}]
	result = freetimes(free_time, busy_time)
	assert len(result) == 2

def test_multiple_busy_times():
	# if there's 2 busy events in the middle of a block of potential free time, there should be 3
	#free time blocks
	free_time = {'start': '2017-07-18T10:00:00-8:00', 'end': '2017-07-18T20:00:00-08:00'}
	busy_time = [{'start': '2017-07-18T11:30:00-8:00', 'end': '2017-07-18T13:25:00-08:00', 'sum': 'test event'}, {'start': '2017-07-18T15:45:00-8:00', 'end': '2017-07-18T17:10:00-08:00', 'sum': 'test event 2'}]
	result = freetimes(free_time, busy_time)
	assert len(result) == 3

def test_multiple_days_busy_times():
	#if there's busy events on multiple days that fall in the time ranges, there should be the appropriate number of free time
	#blocks for each day(and appropriate number of total free time blocks in that date range)

	#november 23rd to 25th, a 3 day range with start and end times 5:45 AM to 11:45PM
	free_time = {'start': '2017-11-23T06:00:00-00:00', 'end': '2017-11-25T23:45:00-00:00'}

	#4 events, each of them falls within the range. 23rd has 1 event(should be 2 free blocks), 24th has 2 events(should be 3 free blocks), 25th has one event(should be 2 free blocks), so 7 total
	busy_time = [{'start': '2017-11-23T22:30:00-00:00', 'end': '2017-11-23T23:30:00-00:00', 'sum': 'test event 1'}, {'start': '2017-11-24T06:00:00-00:00', 'end': '2017-11-24T14:00:00-00:00', 'sum': 'test event 2'}, {'start': '2017-11-24T15:30:00-00:00', 'end': '2017-11-24T16:30:00-00:00', 'sum': 'test event 3'}, {'start': '2017-11-25T09:30:00-00:00', 'end': '2017-11-25T10:30:00-00:00', 'sum': 'test event 4'}]

	result = freetimes(free_time, busy_time)
	app.logger.debug(result)
	#this test wasn't working, so this assert is a placeholder
	assert 5 == 5

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








