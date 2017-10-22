""" Converts ics file to a more nicely formatted one"""
from icalendar import Calendar
from sources import getLocationReplacements
from typing import List, Tuple
import requests

def cleanSummary(summary: str) -> str:
	"""Clean the summary by taking the last piece split by '::'"""
	return summary.split('::')[-1]

def cleanLocation(location: str, replacements: List[Tuple[str,str]]) -> str:
	"""Clean the location by removing the building and room specifications and handling replacements

	Keyword arguments:
	location     -- the location
	replacements -- a list of tuples with pairs of (old, new)
	"""
	new_location = ''.join(location.split('Building: '))
	new_location = ''.join(new_location.split(' Room: '))

	# Replace substrings in the location as set in configuration file
	for pair in replacements:
		new_location = new_location.replace(pair[0], pair[1])
	return new_location

def cleanCalendar(cal: Calendar):
	"""Clean the calendar by cleaning each summary and location"""
	location_replacements = getLocationReplacements() # get the location replacements from file
	for component in cal.walk():
		if component.name == "VEVENT":
			component['summary'] = cleanSummary(component.get('summary'))
			component['location'] = cleanLocation(component.get('location'), location_replacements)

def getUpdatedIcs(source_link):
	"""Entry point that returns a cleaned calendar file"""
	res = requests.get(source_link) # note that this will return an empty calendar if the link is invalid
	cal = Calendar.from_ical(res.text)
	cleanCalendar(cal)
	return cal.to_ical()
