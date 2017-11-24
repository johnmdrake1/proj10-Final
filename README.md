

Project 8 G-Cal free times

Author: John Drake and Michal Young
Collaborators: I again worked with Claire Phillips and Miguel.

Github Profile: https://github.com/johnmdrake1

Repository: https://github.com/johnmdrake1/proj8-freetimes


NOTE: This project was copied and then modified from my project 7, located at the github repo
https://github.com/johnmdrake1/proj7-Gcal. Much of this README is also borrowed from there, but I have made
some notes on my additions in the present project 8. I did remove the test suite for project 7, and added the one for project 8.

Another change that should be noted is proper comparisons for the TIME ranges(for busy times), as opposed to what I had in project
7. In project 7, results were accurate in regard to date, but not in regard to the time range set to be searched each day.
In project 7, the program treated the start and end TIMES as times on the start and end dates(meaning that everything from the 
start time on the start date to the end time on the end date would be searched for events, and not independently for each day
as required by project 7 specifications). My first course of action in completing project 8, and what used much of my development
time, was fixing this issue from project 7 as time accuracy is vital for project 8 to work. I succeeded with this, and split up
inputs for cmp_times into arrow date and time objects, and added new booleans so date and time could be compared independently of
one another. Project 8 now searches each day's time range for busy times. I did not change my project 7 repository to 
implement this fix there, however. As a result project 8 now searches dates and times according to spec, for both busy and
free times!



Description: A program displayed on a webpage through a running server that allows the user to select a date range and 
time range and display busy times in that range based on events from one or more of their google calendars. The time range
is for that time range each day, looked at independently each day. Busy times(events) for each selected calendar
are shown next to that calendar on the page. Below this, Free times are shown. Free times count as any time block in the selected range
that does not have any events that conflict with it.

Instructions:

For end users:
Once the server is up and running, go to localhost:5000 in a web browser. Use the input boxes to select a date range
you want to view data for. Then, select a time range you want to search each date in the date range for for busy, and free, times/events.
Select the "choose" button once these steps are completed. When prompted to log in to google, do so for the account you'd
like to view busy times for. At this point the page should be updated with some additional options, and your date and time range
is now locked in. Here, you may select the check box next to each calendar you would like to view. Please select at least one.
Once you have selected the appropriate check boxes, press the "Submit" button. This will lock in your calendar choices.
The page should now display any busy times in your date range next to the calendar these busy times fall in, for each
of your selected calendars. These will include the name, start time, and end time of each relevant event(in 24h format). 
Below this busy time list, Free time blocks will display in the selected range. It will state which date your free time falls
on, and when your free time starts and goes till. If there are multiple free blocks on the same day, they will
each display on their own line. If you wish to search a different time range or different calendars, change your inputs and hit the choose and/or submit buttons again.

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

index.html is the other primary file, and contains the webpage where inputs and outputs are passed to and from
flask_main.py. Date, time, and a choose button are displayed at first for inputs. Then, available calendars are displayed
on the page with checkboxes next to each, along with a submit button. When the calendars are chosen and submitted, 
events that represent busy times in the chosen range should be displayed right next to their respective calendars for 
all calendars and events. Below the busy times for each calendar, free times will be displayed that do not conflict with 
the busy events in the time range. Seperate jinja operations are used for displaying free times. Some cosmetic changes
have been made here as well, and should make the application look much nicer than project 7.

test_check.py contains a test suite that tests the two new functions in free_times.py. These are freetimes and 
list_freeblocks. "make test" will run these tests. Note that a few were commented out for unknown errors, that were unrelated
to the application's ability to compute the correct result. This is largely due to the difficulty in getting proper parameters
for the calls to freetimes within the test functions, because of the loop-based nature of passing freeblocks as parameters
in the actual application. 

credentials.ini and client_id.json are additional files, necessary for the project to function, that must be added manually 
by the user to the "meetings" directory.

KNOWN BUGS: None which are consistent, everything should function properly. During development, some errors, mainly about strings
as list indeces, would appear for certain inputs but then work perfectly fine when submitted again with the exact same inputs.
This could be due to a variety of factors(browser, time zone, google calendar settings) but they may be completely gone by now 
based on some changes I made to try to fix them.





