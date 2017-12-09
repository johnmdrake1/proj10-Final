

Project 10-MeetMe Meeting Planner Application

Author: John Drake and Michal Young
Collaborators: Got some help from Claire and Miguel.

Github Profile: https://github.com/johnmdrake1

Repository: https://github.com/johnmdrake1/proj10-final

NOTE: Most of the most important commits in terms of my project functionality were made today, Friday December 8th. I submitted 
credentials.ini on Canvas this morning, but made most of my commits after then. Little functionality was available for the versions
on github prior to Friday, but the project is significantly more complete now.


Main error at this point is (bad time) showing up sometimes. I am pretty sure that it wasn't doing this as frequently a couple commits ago,
but can't think of anything I have changed that may have caused this. Looking at my db entries on the mlab dashboard, it 
looks like parts of the date strings may be getting cut off some times, but not every time.


Description: A meeting planning application that features seperate routes and interfaces for meeting planner and meeting attendee. Information
submitted by both parties is added to a MongoDB database on Mlab that is consistently updated until the meeting is finalized 
by the planner. Meeting planner submits their google calendars, chooses which of their free time blocks they would like to propose
as a possible meeting time to their potential attendees, and receives two links for the unique meeting id they have created
(one to send to their attendees, one for the planner themself to view responses and finalize the meeting time once they are 
satisfied with responses). When an attendee follows their respective link, they may log into the google calendar API, choose
their relevant calendars, view their free times in their selected calendars, and choose which of the planner's proposed times they
favor. Finally, the attendee enters their name and submits their response. 

The process ends when the meeting planner uses their exclusive link to choose the proposed time they want based on attendee responses.
Planner submits, and the meeting is finalized preventing further updates or user responses. Planner and attendee will be directed
to a new page showing the finalized meeting time from this point forward.

Instructions:

For the meeting planner:
Once the server is up and running, go to localhost:5000 in a web browser. Use the input boxes to select a date range
you want to view available meeting times for. Then,  Then, select a time range you want to search each date in the date range for for busy, and free, times/events.
Select the "choose" button once these steps are completed. When prompted to log in to google, do so for the account you'd
like to view busy times for. At this point the page should be updated with some additional options, and your date and time range
is now locked in. Here, you may select the check box next to each calendar you would like to view. Please select at least one.
Once you have selected the appropriate check boxes, press the "Submit" button. This will lock in your calendar choices.
The page should now display any busy times in your date range next to the calendar these busy times fall in, for each
of your selected calendars. These will include the name, start time, and end time of each relevant event(in 24h format). 
Below this busy time list, Free time blocks will display in the selected range. It will state which date your free time falls
on, and when your free time starts and goes till. If there are multiple free blocks on the same day, they will
each display on their own line. If you wish to search a different time range or different calendars, change your inputs and hit the choose and/or submit buttons again.

Check the boxes next to the now-displayed free times you want to propose for a meeting, and hit the "new meeting" button
BELOW the boxes. The next page will display a link to send to your attendees, and a unique link for you, the planner. Go to your
planner url to view responses for each proposed time. Select whichever meeting time you prefer once you are ready and satisfied
with the time you have allowed your attendees to respond. Click the submit button(WARNING: This will finalize your meeting,
and no further changes can be made to it!). The next page will show your finalized meeting time. If a late respondent tries
to follow their url, they will also see this page. You should be able to send either link at this point to anyone you wish
to share your finalized time with.

For the potential meeting attendee:
Run the server and follow the link you received from your meeting administrator. Choose a calendar relevant to deciding on a meeting
time. Once you have submitted this form, your free/busy times will be displayed and the meeting admin's preffered times will
now be visible. Decide which one works best for you based on your times, enter your name in the "Name" field, and click the button
to submit. The meeting planner will now be able to view your selections and inputs, and your name will be displayed next to the
time you selected when the planner is viewing from their end. Once the meeting planner has finalized the meeting time based
on you and your fellow attendees' responses, you may follow your link once more to view the time that has been decided on by the
administrator.



For developers:
In project directory, place credentials.ini and client_id.json in the "meetings" folder.

In terminal/command prompt-
1. cd to project directory
2. make install
3. make run (to start server. application can now be accessed in a client/browser by going to localhost:5000.)
4. ctrl+c (to kill server)
5. (optional) type "make test" to run test suite provided in repo

Description of files and application functionality:

flask_main.py is the primary file for the server and its functionality. Here, procedures are put into place
to display the main application page, update this page once date and time ranges are entered, and update this page
again once calendars are selected. There are also functions that handle google api and authentification, functions
that handle the date and time inputs, and functions that retrieve, dissassemble, and compare and evaluate google 
calendar events for busy times. list_events is called when the submit button is pressed in the HTML, which starts
this process of event processing.

Since project 7, a new addition has been added called free_times.py Whereas processing for busy times was handled completely
in flask_main.py, free_times.py is a seperate module and the computations for free times are performed here. Note that
some processing to set up the calls to functions in free_times.py does occur in flask_main.py, as the functions are 
called in flask_main. The bulk of processing was seperated into free_times.py so it could be tested and evaluated independently.
The functions that compute busy times, and their outputs, are used heavily in the calculations for free times (busy times
let us know what times we have free). list_freeblocks(starttime, endtime) simply creates an empty "free block", for each date
that starts and ends at the specified time range. freetimes(freeblock, busytimes) then takes one of these blocks, and a list
of busy times, and uses an algorithm to compute free times based on inputs.

For the final version of the MeetMe project, much has changed. The previous two versions simply displayed the busy and free times
and added no additional functionality once this task had completed. Now, free times may be chosen once they are displayed and a meeting
created. Two urls can be accessed from this point on, and each has its own route of html files. These redirects are handled in 
flask_main, and several new html files are referenced here.

index.html is the other primary file, and contains the webpage where inputs and outputs are passed to and from
flask_main.py. Date, time, and a choose button are displayed at first for inputs. Then, available calendars are displayed
on the page with checkboxes next to each, along with a submit button. When the calendars are chosen and submitted, 
events that represent busy times in the chosen range should be displayed right next to their respective calendars for 
all calendars and events. Below the busy times for each calendar, free times will be displayed that do not conflict with 
the busy events in the time range. Seperate jinja operations are used for displaying free times. Some cosmetic changes
have been made here as well, and should make the application look much nicer than project 7.

In the final project, index.html still serves as the primary page, but will only be used when the meeting planner initializes a 
meeting. All future usage of the application for an incomplete meeting will begin at one of two new urls, user_view.html and
admin_view.html depending on who is accessing the program. Every time a meeting is created and initialized using index.html,
unique urls will be displayed to access these two new html routes. The purpose of a unique url is so different meetings can
be accessed independently. Each meeting will get its own database entry once it has been added, and the database will be modified
whenever its unique urls are accessed.

test_check.py contains a test suite that tests the two new functions in free_times.py. These are freetimes and 
list_freeblocks. "make test" will run these tests. Note that a few were commented out for unknown errors, that were unrelated
to the application's ability to compute the correct result. This is largely due to the difficulty in getting proper parameters
for the calls to freetimes within the test functions, because of the loop-based nature of passing freeblocks as parameters
in the actual application. 

credentials.ini and client_id.json are additional files, necessary for the project to function, that must be added manually 
by the user to the "meetings" directory.

KNOWN BUGS:  During development, some errors, mainly about strings
as list indeces, would appear for certain inputs but then work perfectly fine when submitted again with the exact same inputs.
This could be due to a variety of factors(browser, time zone, google calendar settings) but they may be completely gone by now 
based on some changes I made to try to fix them.

New Meeting button may display twice, click lowest one. In addition to proposed times, an additional time with something
like bad "(bad date)" "(bad time)" may appear. This can be ignored as it should not affect functionality for the times that actually
were chosen.

Sometimes (bad date) (bad time) shows up on meeting.html for one or more of the chosen proposal times. This seems to happen at random,
and has something to do with the datetime strings being cut off as far as I know. There seems to always be an extra "proposed time"
with the bad date/time message, seemingly caused by an empty time being added to the list. 

bad time appears most frequently on the page for a finalized meeting. Even if the proposed time displayed properly on the pages leading
up to the final page, it will often not display correctly on final.html. Most of the time, this is for the end time of the finalized
meeting, but sometimes it shows for begin date and/or time as well. This really does seem to happen at random, and not every time.




