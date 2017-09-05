'''Loads sources from a specified source'''
import csv
import os

# Get source username from the source dictionary
def getCalendarUrl(username: str) -> str:
	calendar_sources = {}
	with open(os.path.join(os.path.dirname(__file__), '../sources.csv'), 'r') as infile:
		reader = csv.reader(infile)
		next(reader, None) # skip the headers
		calendar_sources = {rows[0]:rows[2] for rows in reader}
	return calendar_sources[username]
