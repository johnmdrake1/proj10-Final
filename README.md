

Project 7 G-Cal busy times

Author: John Drake and Michal Young
Collaborators: I worked with Claire Phillips and Miguel

Repository: https://github.com/johnmdrake1/proj7-Gcal

Github Profile: https://github.com/johnmdrake1

Notes on lateness: By the 10% late penalty deadline(Thursday, November 16 at 8:00pm I had everything requiredin the repository
with the exception of the folowing:
1. This README
2. A completed test suite
3. Adequate comments in the code explaining what it does

Aside from these missing pieces, I thought the project was working with the commit early on Thursday in the AM. What I somehow did 
not realize through my testing, however, was that the events being displayed were not correct most of the time and only start
dates AFTER the events had happened would display them. I did not realize this until after the late deadline on Thursday,
but when I went to debug the problem ended up being extremely trivial; a less than sign that should have been a greater
than sign in a boolean variable in cmp_times. Once flipping this sign, the project functions according to spec. There is a commit
submitted Friday that reflects this change, and nothing else. As it was such a small error I hope that this late commit can be 
considered when grading my project on functionality. I regret making a mistake with such large consequences and not discovering it
until it was too late.

Besides the greater than/less than commit, I will list any further changes I have made after the late deadline below:
1. Added this README
2. Added comments in code(index.html and flask_main.py)



Description: A program displayed on a webpage through a running server that allows the user to select a date range and 
time range and display busy times in that range based on events from one or more of their google calendars. The time range
is for that time range each day, looked at independently each day. Busy times(events) for each selected calendar
are shown next to that calendar on the page.

Instructions:

For end users:
Once the server is up and running, go to localhost:5000 ina  web browser. Use the boxes to select a date range
you want to view data for. Then, select a time range you want to search each date in the date range for for busy times/events.
Select the "choose" button once these steps are completed. When prompted to log in to google, do so for the account you'd
like to view busy times for. At this point the page should be updated with some additional options, and your date and time range
is now locked in. Here, you may select the check box next to each calendar you would like to view. Please select at least one.
Once you have selected the appropriate check boxes, press the "Submit" button. This will lock in your calendar choices.
The page should now display any busy times in your date range next to the calendar these busy times fall in, for each
of your selected calendars. These will include the name, start time, and end time of each relevant event(in 24h format). If you 
wish to search a different time range or different calendars, change your inputs and hit the choose and/or submit buttons again.

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
again once calendar are selected. There are also functions that handle google api and authentification, functions
that handle the date and time inputs, and functions that retrieve, dissassemble, and compare and evaluate google 
calendar events for busy times. list_events is called when the submit button is pressed in the HTML, which starts
this process of event processing.

index.html is the other primary file, and contains the webpage where inputs and outputs are passed to and from
flask_main.py. Date, time, and a choose button are displayed at first for inputs. Then available calendars are displayed
on the page with checkboxes next to each, along with a submit button. When the calendars are chosen and submitted, 
events that represent busy times in the chosen range should be displayed right next to their respective calendars for 
all calendars and events.

test_check.py contains a test suite that tests the cmp_times function in flask_main.py by implementing python nose tests.
These can be run by the command "make test", while in the root project directory.

credentials.ini and client_id.json are additional files, necessary for the project to function, that must be added manually 
by the user to the "meetings" directory.





