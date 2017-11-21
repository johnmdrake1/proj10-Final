# Date handling 
import arrow # Replacement for datetime, based on moment.js

import flask
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


def list_freeblocks(starttime, endtime):
	# Will make a list of available time blocks. This will be the entire possible range for each date in the range that is set, so it will be the
	# same for each day.


	#starttime as an arrow object
	st = arrow.get(starttime)
	#endtime as an arrow object
	et = arrow.get(endtime)
	#hours for each end time
	eth = int(et.format("H"))
	#minute for each end time
	etm = int(et.format("m"))
	#curdate for iterating through while loop, set equal to st
	curdate = st
	#empty list for freeblocks
	freeblocks = []

	#adds a block for all possible free times for each day in range to a list
	while (curdate <= et):
		

		#make end time
		end = curdate.replace(hour=eth, minute=etm)

		app.logger.debug(end)



		#dictionary with start and end times for each date in range
		todict = {'start': curdate.isoformat() , 'end': end.isoformat()}
		#add dict to return list
		freeblocks.append(todict)
		#add one to the day
		curdate = curdate.shift(days=+1)



	return freeblocks





def freetimes(busytimes, freeblocks):
	# Calculate free times based on the time blocks of potential free time, and the busy times/events that block and prevent the possibility
	# of a time being available.

	return None