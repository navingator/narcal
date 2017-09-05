#!/usr/bin/env python3
'''Entry point for the server'''

from bottle import run
from dotenv import load_dotenv
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'app/')) # Add files for import
import routes

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Listen on the specified port
run(host=os.environ.get('HOST'), port=os.environ.get('PORT'))