""" Converts ics file to a more nicely formatted one"""
from icalendar import Calendar
import requests

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

def getUpdatedIcs(source_link):
	res = requests.get(source_link) # note that this will return an empty calendar if the link is invalid
	cal = Calendar.from_ical(res.text)
	cleanCalendar(cal)
	return cal.to_ical()
