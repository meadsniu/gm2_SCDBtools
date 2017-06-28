"""
insert_subchannels.py

Python script to insert subchannel information from a csv file
into the g-2 online database.

M. Eads
June 2017
"""

import psycopg2

# create the connection to the database
conn = psycopg2.connect("dbname=gm2_online_prod user=gm2_writer host=localhost port=5433")

infile = open('g2sc_subchannels_MGattone_6-19_UPDATED.csv')

for line in infile:
    if line.split(',')[1] == 'test_channel': continue
    #print "* line:",
    #print line
    splitline = line.rstrip().split(',')
    #print 'splitline:', splitline
    if splitline[0] == 'id' or len(splitline[1]) == 0: continue
    channel = splitline[1]
    index = splitline[2]
    if channel == 'test_channel' and index == 0: continue
    subchannel = splitline[3]
    name = splitline[4]
    description = splitline[5]
    isAttached = splitline[8]
    isValid = splitline[9]
    display_name = splitline[10]
    #print '**parsed values:', channel, index, subchannel, name, description, isAttached, isValid, display_name

    sql = 'INSERT INTO g2sc_subchannels (channel, index, subchannel, name, description, "isAttached", "isValid", display_name) '
    sql += "VALUES ("
    sql += "'" + channel + "', "
    sql += index + ", "
    sql += "'" + subchannel + "', "
    sql += "'" + name + "', "
    sql += "'" + description + "', "
    sql += isAttached + ", "
    sql += isValid + ", "
    sql += "'" + display_name + "'"
    sql += ");"

    print sql
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()

conn.close()
