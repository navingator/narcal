'''Routes and controllers for HTTP server'''
from bottle import abort, response, route
from narcal import get_updated_ics
from sources import get_calendar_url
import csv

@route('/<username>')
def getCalendar(username:str):
	# Check if the username exists in the 'database'
	calendarUrl = ''
	try:
		calendarUrl = get_calendar_url(username)
	except KeyError:                  # Username not found in dictionary
		abort(404, "Username not found.")
	except FileNotFoundError:         # Could not find a file containing sources
		abort(500, "Source file not found")
	except (csv.Error, IndexError):   # The file containing the sources was incorrectly configured
		abort(500, "Sources configured incorrectly. Contact the site admin for help.")
	# Return the calendar for that username
	try:
		ics = get_updated_ics(calendarUrl)
	except: 
		abort(500, "Error retrieving data from source. Check that one45 is up and source file is configured correctly.")

	# set response headers and return value
	response.content_type = 'text/calendar; charset=utf-8'
	response.headers['Content-Disposition'] = 'inline; filename=' + username + '.ics'
	return ics