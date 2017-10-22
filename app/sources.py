'''Loads sources from a specified source'''
import csv
import os
from typing import List, Tuple

# Get source username from the source dictionary
def getCalendarUrl(username: str) -> str:
	"""Gets a calendar URL from a source csv file"""
	calendar_sources = {}
	with open(os.path.join(os.path.dirname(__file__), '../config/sources.csv'), 'r') as infile:
		reader = csv.reader(infile)
		next(reader, None) # skip the headers
		calendar_sources = {rows[0]:rows[2] for rows in reader}
	return calendar_sources[username]

# Get a list of tuples containing location replacements in the format (old, new)
def getLocationReplacements() -> List[Tuple[str,str]]:
	"""Gets a list of location replacement tuples from csv"""
	replacements = []
	with open(os.path.join(os.path.dirname(__file__), '../config/location.replacements.csv'), 'r') as infile:
		reader = csv.reader(infile)
		next(reader, None) # skip the headers
		replacements = [(rows[0], rows[1]) for rows in reader]
	return replacements