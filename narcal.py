#!/usr/bin/env python3
""" Converts ics file to a more nicely formatted one"""
from icalendar import Calendar
import os

def cleanSummary(summary: str) -> str:
	return summary.split('::')[-1]

def cleanLocation(location: str) -> str:
	new_location = ''.join(location.split('Building: '))
	new_location = ''.join(new_location.split(' Room: '))
	return new_location

def cleanCalendar(cal: Calendar):
	for component in cal.walk():
		if component.name == "VEVENT":
			component['summary'] = cleanSummary(component.get('summary'))
			component['location'] = cleanLocation(component.get('location'))

def writeIcs(cal: Calendar, filename: str):
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'wb') as f:
		f.write(cal.to_ical())

# TODO replace with file retrieved from http request
with open('./samples/source.ics', 'rb') as source_file:
	cal = Calendar.from_ical(source_file.read())
	cleanCalendar(cal)
	writeIcs(cal,'./dist/sample/output.ics')
