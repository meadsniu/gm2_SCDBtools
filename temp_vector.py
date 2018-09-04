"""
temp_vector.py

This Script is to find any temperature imbalnce in the magnet and to see if this changes with time.

This is a continuation of the work done by Mike Eads and Gavin Dunn

B. Kelly
June 2018
"""

import psycopg2
import ROOT
import SCDButil
import time
import cmath

time_interval = 'day'
if time_interval == 'hour':
	begTime = time.time() - 3600
elif time_interval == 'day':
	begTime = time.time() - 86400
elif time_interval == 'week':
	begTime = time.time() - 604800
elif time_interval == 'month':
	begTime = time.time() - 2678400
elif time_interval == 'year':
	begTime = time.time() - 3153600
elif time_interval == 'all':
	begTime = time.time() - 315360000

db = SCDButil.SCDButil(calib=True)

vector = db.temp_vector(time_interval = time_interval)
#temperature_map=db.temp_map(vector)
#vector actually holds the timetemp dictionary used to make the vector, which temp_map needs to run

