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





def freetimes(freeblock, busytimes):
    # Calculate free times based on the time blocks of potential free time, and the busy times/events that block and prevent the possibility
    # of a time being available.
    # free_times = []
    # free_blocks = list_freeblocks(starttime, endtime)
    # app.logger.debug(free_blocks)

    # #subtract free blocks from busy times
    # if busytimes == []:
    #   app.logger.debug("all time is free(case a or e for every day)")
    #   free_times = free_blocks
    #   return free_times

    app.logger.debug("FreeBLock{}:".format(freeblock))
    app.logger.debug("Busy{}:".format(busytimes))

    #added this to handle test case with empty freeblock, don't believe it broke anything but I can't be sure
    if freeblock == []:
        freetimes_in_block = []
        return freetimes_in_block

    freetimes_in_block = []
    freeblockstart = freeblock['start']
    freeblockend = freeblock['end']
    for event in busytimes:
        #app.logger.debug("placeholder")

        eventstart = event['start']
        eventend = event['end']

        # Case F
        if (eventstart <= freeblockstart) and (eventend >= freeblockend):
            app.logger.debug("CASE F")
            return freetimes_in_block
        # Case B
        elif (eventstart <= freeblockstart) and (eventend > freeblockstart) and (eventend < freeblockend):
            app.logger.debug("CASE B")
            freeblockstart = eventend
        # Case C
        elif (eventstart > freeblockstart) and (eventend < freeblockend):
            app.logger.debug("This is a new freeblock CASE C")
            new_freeblock = { "start": freeblockstart, "end": eventstart }
            freetimes_in_block.append(new_freeblock)
            
            freeblockstart = eventend
        # Case D
        elif (eventstart > freeblockstart) and (eventstart < freeblockend) and (eventend >= freeblockend):
            app.logger.debug("CASE D")
            freeblockend = eventstart
        else:
            app.logger.debug("SOMETHING IS WRONG!")

    if (freeblockstart >= freeblock['start']) and (freeblockend <= freeblock['end']):
        new_freeblock = { "start": freeblockstart, "end": freeblockend }
        freetimes_in_block.append(new_freeblock)
    else:
        return freetimes_in_block

    return freetimes_in_block



    # else:
    #   for event in busytimes:
    #       app.logger.debug("Start outer loop")
    #       busy_start = arrow.get(event['start'])
    #       busy_end = arrow.get(event['end'])
    #       for block in free_blocks:
    #           block_start = arrow.get(block['start'])
    #           block_end = arrow.get(block['end'])
    #           if (busy_start <= block_start) and (busy_end >= block_end):
    #               app.logger.debug("no busy time on a day")
    #               app.logger.debug(busy_start)
    #               app.logger.debug(block_start)
    #           elif (busy_start <= block_start) and (busy_end < block_end):


    # for block in free_times:
    #   for event in busytimes:
    #       if event['start'] < block['start'] and event['end'] < block['start']:
    #           isfree = True
    #       elif event['start'] > block['start'] and event['start'] < block['end']:
    #           isfree = False
    #       if isfree = True:
    #           free_times.append(block)



    

    # return None