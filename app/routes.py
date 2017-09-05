'''Routes and controllers for HTTP server'''
from bottle import abort, response, route
from narcal import getUpdatedIcs
from sources import getCalendarUrl
import csv

@route('/<username>')
def getCalendar(username:str):
	# Check if the username exists in the 'database'
	calendarUrl = ''
	try:
		calendarUrl = getCalendarUrl(username)
	except KeyError:
		abort(404, "Username not found.")
	except FileNotFoundError:
		abort(500, "Source file not found")
	except (csv.Error, IndexError):
		abort(500, "Sources configured incorrectly. Contact the site admin for help.")
	# Return the calendar for that username
	try:
		ics = getUpdatedIcs(calendarUrl)
	except: 
		abort(500, "Error retrieving data from source. Check that one45 is up and source file is configured correctly.")

	# set response headers and return value
	response.content_type = 'text/calendar; charset=utf-8'
	response.headers['Content-Disposition'] = 'inline; filename=' + username + '.ics'
	return ics