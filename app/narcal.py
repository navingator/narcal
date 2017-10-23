""" Converts ics file to a more nicely formatted one"""
from icalendar import Calendar
from sources import get_location_replacements
from typing import List, Tuple
import requests
import re

def shorten_summary(summary: str) -> str:
	"""Shorten the summary by removing unnecessary first element and numbering"""
	split_summary = summary.split(':')

	# abort if the structure is unknown at this point
	if len(split_summary) == 1: 
		return summary
	
	# clear the first part, unless it contains the word "optional" as a qualifier
	if "optional" not in split_summary[0]:
		split_summary[0] = ''
	
	""" 
	remove the numbering from the description by removing when matching 
	at least one digit followed by a period and optionally a space 
	"""
	split_summary[1] = re.sub(r'^[0-9]+\.\s?', '', split_summary[1])

	# rejoin the summary 
	new_summary = ':'.join(split_summary)
	if new_summary[0] == ':': # handle the case when the 0th element was removed
		new_summary = new_summary[1:]

	return new_summary

def clean_summary(summary: str) -> str:
	"""Cleans the summary by removing unhelpful components"""

	# Remove larger useless chunks by taking the last piece split by '::'
	new_summary = summary.split('::')[-1] # will include just the last section or everything if it doesn't find '::'

	return shorten_summary(new_summary)

def clean_location(location: str, replacements: List[Tuple[str,str]]) -> str:
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

def clean_calendar(cal: Calendar):
	"""Clean the calendar by cleaning each summary and location"""
	location_replacements = get_location_replacements() # get the location replacements from file
	for component in cal.walk():
		if component.name == "VEVENT":
			component['summary'] = clean_summary(component.get('summary'))
			component['location'] = clean_location(component.get('location'), location_replacements)

def get_updated_ics(source_link):
	"""Entry point that returns a cleaned calendar file"""
	res = requests.get(source_link) # note that this will return an empty calendar if the link is invalid
	cal = Calendar.from_ical(res.text)
	clean_calendar(cal)
	return cal.to_ical()
