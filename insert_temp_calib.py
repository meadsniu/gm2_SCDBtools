"""
insert_subchannels.py

Python script to insert subchannel information from a csv file
into the g-2 online database.

M. Eads
June 2017
"""

import psycopg2

write_to_db = True

# create the connection to the database
conn = psycopg2.connect("dbname=gm2_online_prod user=gm2_writer host=localhost port=5433")

#infile = open('CalibrationReferenceData-AirDiff.csv')
infile = open('TempCalibration_jul2018.csv')

# version 2 is using the data taken in summer 2017
# version 3 is using the data taken in summer 2018
version = '3'

for line in infile:
    if line.split(',')[1] == 'test_channel': continue
    #print "* line:",
    #print line
    splitline = line.rstrip().split(',')
    #splitline = line.split(',')
    print 'splitline:', splitline
    if splitline[0] == 'subchannel' or len(splitline[1]) == 0: continue
    subchannel = splitline[0]
    value = splitline[1]

    print subchannel, value

    sql = 'INSERT INTO g2sc_calib_temp (subchannel, calib_value, version) '
    sql += "VALUES ("
    sql += "'" + subchannel + "', "
    sql += value + " "
    sql += ", " + version + " " 
    sql += ");"

    print sql
    if write_to_db:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()

conn.close()
