import flask
from flask import render_template
from flask import request
from flask import url_for
import uuid

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
# import datetime # But we still need time
from dateutil import tz  # For interpreting local times


# OAuth2  - Google library implementation for convenience
from oauth2client import client
import httplib2   # used in oauth2 flow

# Google API for services 
from apiclient import discovery

#new free times file
from free_times import list_freeblocks, freetimes

###
# Globals
###
import config
if __name__ == "__main__":
    CONFIG = config.configuration()
else:
    CONFIG = config.configuration(proxied=True)

app = flask.Flask(__name__)
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)
app.secret_key=CONFIG.SECRET_KEY

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = CONFIG.GOOGLE_KEY_FILE  ## You'll need this
APPLICATION_NAME = 'MeetMe class project'

#############################
#
#  Pages (routed from URLs)
#
#############################

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Entering index")
  if 'begin_date' not in flask.session:
    init_session_values()
  return render_template('index.html')

@app.route("/choose")
def choose():
    ## We'll need authorization to list calendars 
    ## I wanted to put what follows into a function, but had
    ## to pull it back here because the redirect has to be a
    ## 'return' 
    app.logger.debug("Checking credentials for Google calendar access")
    credentials = valid_credentials()
    if not credentials:
      app.logger.debug("Redirecting to authorization")
      return flask.redirect(flask.url_for('oauth2callback'))

    gcal_service = get_gcal_service(credentials)
    app.logger.debug("Returned from get_gcal_service")
    flask.g.calendars = list_calendars(gcal_service)
    
    return render_template('index.html')

@app.route("/choose2")
def choose2():
    # Same as choose, but calls get_events instead of list_calendars. This is so the events can
    # be listed on index.html instead of being redirected to a new page. 
    app.logger.debug("Checking credentials for Google calendar access")
    credentials = valid_credentials()
    if not credentials:
      app.logger.debug("Redirecting to authorization")
      return flask.redirect(flask.url_for('oauth2callback'))

    gcal_service = get_gcal_service(credentials)
    app.logger.debug("Returned from get_gcal_service")
    flask.g.calendars = list_calendars(gcal_service)
    flask.g.events = get_events(gcal_service)
    flask.g.free = flask.session['free']
    
    return render_template('index.html')


####
#
#  Google calendar authorization:
#      Returns us to the main /choose screen after inserting
#      the calendar_service object in the session state.  May
#      redirect to OAuth server first, and may take multiple
#      trips through the oauth2 callback function.
#
#  Protocol for use ON EACH REQUEST: 
#     First, check for valid credentials
#     If we don't have valid credentials
#         Get credentials (jump to the oauth2 protocol)
#         (redirects back to /choose, this time with credentials)
#     If we do have valid credentials
#         Get the service object
#
#  The final result of successful authorization is a 'service'
#  object.  We use a 'service' object to actually retrieve data
#  from the Google services. Service objects are NOT serializable ---
#  we can't stash one in a cookie.  Instead, on each request we
#  get a fresh serivce object from our credentials, which are
#  serializable. 
#
#  Note that after authorization we always redirect to /choose;
#  If this is unsatisfactory, we'll need a session variable to use
#  as a 'continuation' or 'return address' to use instead. 
#
####

def valid_credentials():
    """
    Returns OAuth2 credentials if we have valid
    credentials in the session.  This is a 'truthy' value.
    Return None if we don't have credentials, or if they
    have expired or are otherwise invalid.  This is a 'falsy' value. 
    """
    if 'credentials' not in flask.session:
      return None

    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials'])

    if (credentials.invalid or
        credentials.access_token_expired):
      return None
    return credentials


def get_gcal_service(credentials):
  """
  We need a Google calendar 'service' object to obtain
  list of calendars, busy times, etc.  This requires
  authorization. If authorization is already in effect,
  we'll just return with the authorization. Otherwise,
  control flow will be interrupted by authorization, and we'll
  end up redirected back to /choose *without a service object*.
  Then the second call will succeed without additional authorization.
  """
  app.logger.debug("Entering get_gcal_service")
  http_auth = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http_auth)
  app.logger.debug("Returning service")
  return service

@app.route('/oauth2callback')
def oauth2callback():
  """
  The 'flow' has this one place to call back to.  We'll enter here
  more than once as steps in the flow are completed, and need to keep
  track of how far we've gotten. The first time we'll do the first
  step, the second time we'll skip the first step and do the second,
  and so on.
  """
  app.logger.debug("Entering oauth2callback")
  flow =  client.flow_from_clientsecrets(
      CLIENT_SECRET_FILE,
      scope= SCOPES,
      redirect_uri=flask.url_for('oauth2callback', _external=True))
  ## Note we are *not* redirecting above.  We are noting *where*
  ## we will redirect to, which is this function. 
  
  ## The *second* time we enter here, it's a callback 
  ## with 'code' set in the URL parameter.  If we don't
  ## see that, it must be the first time through, so we
  ## need to do step 1. 
  app.logger.debug("Got flow")
  if 'code' not in flask.request.args:
    app.logger.debug("Code not in flask.request.args")
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
    ## This will redirect back here, but the second time through
    ## we'll have the 'code' parameter set
  else:
    ## It's the second time through ... we can tell because
    ## we got the 'code' argument in the URL.
    app.logger.debug("Code was in flask.request.args")
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    ## Now I can build the service and execute the query,
    ## but for the moment I'll just log it and go back to
    ## the main screen
    app.logger.debug("Got credentials")
    return flask.redirect(flask.url_for('choose'))

#####
#
#  Option setting:  Buttons or forms that add some
#     information into session state.  Don't do the
#     computation here; use of the information might
#     depend on what other information we have.
#   Setting an option sends us back to the main display
#      page, where we may put the new information to use. 
#
#####

@app.route('/setrange', methods=['POST'])
def setrange():
    """
    User chose a date range with the bootstrap daterange
    widget.
    """




    app.logger.debug("Entering setrange")  
    flask.flash("Setrange gave us '{}'".format(
      request.form.get('daterange')))
    daterange = request.form.get('daterange')
    flask.session['daterange'] = daterange
    #time values are got here, need to get them to cmp_times
    start_clock = request.form.get('start_clock')
    app.logger.debug(start_clock)
    end_clock = request.form.get('end_clock')
    app.logger.debug(end_clock)
    flask.session['start_clock'] = start_clock
    flask.session['end_clock'] = end_clock
    daterange_parts = daterange.split()
    flask.session['begin_date'] = interpret_date(daterange_parts[0])
    flask.session['end_date'] = interpret_date(daterange_parts[2])
    app.logger.debug("Setrange parsed {} - {}  dates as {} - {}".format(
      daterange_parts[0], daterange_parts[1], 
      flask.session['begin_date'], flask.session['end_date']))
    return flask.redirect(flask.url_for("choose"))

####
#
#   Initialize session variables 
#
####

def init_session_values():
    """
    Start with some reasonable defaults for date and time ranges.
    Note this must be run in app context ... can't call from main. 
    """
    # Default date span = tomorrow to 1 week from now
    now = arrow.now('local')     # We really should be using tz from browser
    tomorrow = now.replace(days=+1)
    nextweek = now.replace(days=+7)
    flask.session["begin_date"] = tomorrow.floor('day').isoformat()
    flask.session["end_date"] = nextweek.ceil('day').isoformat()
    flask.session["daterange"] = "{} - {}".format(
        tomorrow.format("MM/DD/YYYY"),
        nextweek.format("MM/DD/YYYY"))
    # Default time span each day, 8 to 5
    #now 12-12, did this in a different part of the code
    flask.session["begin_time"] = interpret_time("9am")
    flask.session["end_time"] = interpret_time("5pm")

def interpret_time( text ):
    """
    Read time in a human-compatible format and
    interpret as ISO format with local timezone.
    May throw exception if time can't be interpreted. In that
    case it will also flash a message explaining accepted formats.
    """
    app.logger.debug("Decoding time '{}'".format(text))
    time_formats = ["ha", "h:mma",  "h:mm a", "H:mm"]
    try: 
        as_arrow = arrow.get(text, time_formats).replace(tzinfo=tz.tzlocal())
        as_arrow = as_arrow.replace(year=2016) #HACK see below
        app.logger.debug("Succeeded interpreting time")
    except:
        app.logger.debug("Failed to interpret time")
        flask.flash("Time '{}' didn't match accepted formats 13:30 or 1:30pm"
              .format(text))
        raise
    return as_arrow.isoformat()
    #HACK #Workaround
    # isoformat() on raspberry Pi does not work for some dates
    # far from now.  It will fail with an overflow from time stamp out
    # of range while checking for daylight savings time.  Workaround is
    # to force the date-time combination into the year 2016, which seems to
    # get the timestamp into a reasonable range. This workaround should be
    # removed when Arrow or Dateutil.tz is fixed.
    # FIXME: Remove the workaround when arrow is fixed (but only after testing
    # on raspberry Pi --- failure is likely due to 32-bit integers on that platform)


def interpret_date( text ):
    """
    Convert text of date to ISO format used internally,
    with the local time zone.
    """
    try:
      as_arrow = arrow.get(text, "MM/DD/YYYY").replace(
          tzinfo=tz.tzlocal())
    except:
        flask.flash("Date '{}' didn't fit expected format 12/31/2001")
        raise
    return as_arrow.isoformat()

def next_day(isotext):
    """
    ISO date + 1 day (used in query to Google calendar)
    """
    as_arrow = arrow.get(isotext)
    return as_arrow.replace(days=+1).isoformat()

####
#
#  Functions (NOT pages) that return some information
#
####
  
def list_calendars(service):
    """
    Given a google 'service' object, return a list of
    calendars.  Each calendar is represented by a dict.
    The returned list is sorted to have
    the primary calendar first, and selected (that is, displayed in
    Google Calendars web app) calendars before unselected calendars.
    """
    app.logger.debug("Entering list_calendars")  
    calendar_list = service.calendarList().list().execute()["items"]
    result = [ ]
    for cal in calendar_list:
        kind = cal["kind"]
        id = cal["id"]
        if "description" in cal: 
            desc = cal["description"]
        else:
            desc = "(no description)"
        summary = cal["summary"]
        # Optional binary attributes with False as default
        selected = ("selected" in cal) and cal["selected"]
        primary = ("primary" in cal) and cal["primary"]
        

        result.append(
          { "kind": kind,
            "id": id,
            "summary": summary,
            "selected": selected,
            "primary": primary
            })
    return sorted(result, key=cal_sort_key)



    


def cal_sort_key( cal ):
    """
    Sort key for the list of calendars:  primary calendar first,
    then other selected calendars, then unselected calendars.
    (" " sorts before "X", and tuples are compared piecewise)
    """
    if cal["selected"]:
       selected_key = " "
    else:
       selected_key = "X"
    if cal["primary"]:
       primary_key = " "
    else:
       primary_key = "X"
    return (primary_key, selected_key, cal["summary"])

@app.route('/list_events', methods=['POST'])
def list_events():
  #Despite the possibly misleading function name, this function serves only to
  #get the calendar ids of the calendars whose checkboxes were filled prior to user submission
  #using the submit button. The result, stored in a session variable, is a list.
  flask.session["selected"] = request.form.getlist("calcheck")
  #choose2 is called to update index.html with new content retrieved here, to be displayed below what 
  #was already there
  return flask.redirect(flask.url_for("choose2"))
  


def get_events(service):
  # This function actually retrieves the events themselves. This includes id and events with descriptions.
  # Start and end times/dates are retrieved and set here to be used in future computations, which are not
  # performed here in get_events.


  cal_list = flask.session["selected"]
  eve_list = []
  #starttime = arrow.get(flask.session['begin_time']).time().isoformat()
  app.logger.debug(flask.session['start_clock'])
  # test = flask.session['start_clock'] + ':00'
  #app.logger.debug(test)
  #start time from user input
  starttime = flask.session['start_clock']
  app.logger.debug(starttime)
  #endtime = arrow.get(flask.session['end_time']).time().isoformat()
  #end time from user input
  endtime = flask.session['end_clock']
  app.logger.debug(endtime)
  #start clock needs to be the new value for start_time and end_time
  # app.logger.debug(flask.session['start_clock'])
  begin_date = flask.session["begin_date"]
  app.logger.debug(begin_date)
  end_date = flask.session["end_date"]
  app.logger.debug(end_date)
  startdate = begin_date[:11] + starttime + begin_date[19:]
  app.logger.debug(startdate)
  enddate = end_date[:11] + endtime + end_date[19:]
  app.logger.debug(enddate)
  app.logger.debug("DATES {}, {}".format(startdate, enddate))
  

  for ids in cal_list:
    #Gets the events for an individual calendar. This loop loops through the SELECTED calendars and gets the events in each.
    #this variable "events" is only the list of events in the current calendar in this iteration of the loop.
    events = service.events().list(calendarId=ids).execute()["items"]
    #eve_list.append(events)
    # app.logger.debug("calendar events")
    
    #cmp_times, the function that actually performs the comparisons and computations to get results, is called here
    #using the events in the current calendar and start and end date/times defined earlier in get_events. The result of the call
    #to get_times is stored here, and contains the events to display as busy times.
    result = cmp_times(events, startdate, enddate)
    #get free blocks
    freeblocks = list_freeblocks(startdate, enddate)

    #get free times
    #pre-output
    freetimeslist = []
    #output list
    finalfreelist = []

    #if no busy events at all, FREE TIME ALL DAY 
    if result == []:
        freetimeslist = freeblocks



    # iterate through each free block 
    for block in freeblocks:
        #get busy events in that block
        busyevents = cmp_times(events, block['start'], block['end'])
        #getting the free times in that block
        #call freetimes, set result to freetimes_list
        freetimes_list = freetimes(block, busyevents)
        #if there are free times(list not empty), add them to the list of free times
        if freetimes_list != []:
            for time in freetimes_list:
                freetimeslist.append(time)

    #eve_list is a list of dictionaries. Each dictionary represents one of the selected calendar and stores all of the events
    #in that calendar which qualify as busy times. The list as a whole (eve_list) contains all of the selected calendars and the busy 
    #times for each. This is because more than one calendar can be selected to display busy times for.
    #

    #gets all free times for that calendar and adds them to a "final" list (to be iterated through in jinja)
    finalfreelist.append({"id": id, "free_times": freetimeslist})





    eve_list.append(
    {
        "id": ids,
        "events": result
    })

    # app.logger.debug(events)
    # eve_list.append(events)
    app.logger.debug(eve_list)



  #get_events is called in choose2 to display results on webpage
  return eve_list

def cmp_times(events, starttime, endtime):
  #list that will contain busy events
  busylist = []
  arsdate = arrow.get(starttime).date()
  app.logger.debug(arsdate)
  aredate = arrow.get(endtime).date()
  app.logger.debug(aredate)
  arstime = arrow.get(starttime).time()
  app.logger.debug(arstime)
  aretime = arrow.get(endtime).time()
  app.logger.debug(aretime)

  #return "no events" if the list of all events passed to cmp_times is empty(the first parameter)
  if events==[]:
    return "no events"
  
  for event in events:
    #only account for events that are not transparent in calculating busy times

    if "transparency" not in event:
      if "date" in event["start"]:
        #what the event is 
        summary = event["summary"]
        #event begin time
        eventBegin = event["start"]["date"] + "00:00:00" + starttime[19:]
        #event end time
        eventEnd = event["end"]["date"] + "23:59:00" + endtime[19:]


      else:
        #what the event is
        summary = event["summary"]
        #event begin time
        eventBegin = event["start"]["dateTime"]
        eventBegindate = arrow.get(eventBegin).date()
        eventBegintime = arrow.get(eventBegin).time()

        app.logger.debug(eventBegin)
        app.logger.debug(eventBegindate)
        app.logger.debug(eventBegintime)
        #event end time
        eventEnd = event["end"]["dateTime"]
        #arrow object for event end date only
        eventEnddate = arrow.get(eventEnd).date()
        #arrow object for event end time only
        eventEndtime = arrow.get(eventEnd).time()
        app.logger.debug(eventEnd)
        app.logger.debug(eventEnddate)
        app.logger.debug(eventEndtime)
      #three possible cases for events that should be included
      # app.logger.debug(starttime)
      # app.logger.debug(endtime)
      # app.logger.debug(eventBegin)

      #if event starts after the start of the selected time range, and ends after the end time of the range
      #added 2 new booleans on each. It now checks for date and time independently, as seperate arrow objects.
      r1 = ((eventBegindate >= arsdate) and (eventEnddate <= aredate)) and ((eventBegintime >= arstime) and (eventEndtime <= aretime))
      #r1 = (eventBegin >= starttime) and (eventEnd < endtime)
      #if event begins before the start time but ends after the start time, making it so there's some busy time relevant to the event
      r2 = ((eventBegindate <= arsdate) and (eventEnddate >= arsdate)) and ((eventBegintime <= arstime) and (eventEndtime >= arstime))
      #r2 = (eventBegin < starttime) and (eventEnd > starttime)
      #if event begins before the end time but ends after the end time
      r3 = ((eventBegindate <= aredate) and (eventEnddate >= aredate)) and ((eventBegintime <= aretime) and (eventEndtime >= aretime))
      #r3 = (eventBegin < endtime) and (eventEnd > endtime)

      #if any of these three booleans evaluate to true, they should be included as busy times.
      if (r1 or r2 or r3):
        #sum(name of event), start time for the event, end time for the event stored in a dictionary and displayed on the webpage as the 
        #same key:value pairs
        event = {"sum":summary, "start":eventBegin, "end": eventEnd}
        #add each dictionary to the list of busy times
        busylist.append(event)

    else:
      return "no events"

  #return the list of busy times, the function get_times uses this returned list to eventually display on the webpage
  return busylist








  
  

  






#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try:
        normal = arrow.get( time )
        return normal.format("HH:mm")
    except:
        return "(bad time)"
    
#############


if __name__ == "__main__":
  # App is created above so that it will
  # exist whether this is 'main' or not
  # (e.g., if we are running under green unicorn)
  app.run(port=CONFIG.PORT,host="0.0.0.0")
    
