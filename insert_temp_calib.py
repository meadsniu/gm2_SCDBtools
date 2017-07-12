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

infile = open('SubchannelCailbrationBreakdown_7-11_Fitted.csv')

for line in infile:
    if line.split(',')[1] == 'test_channel': continue
    #print "* line:",
    #print line
    splitline = line.rstrip().split(',')
    #print 'splitline:', splitline
    if splitline[0] == 'Subchannel' or len(splitline[1]) == 0: continue
    subchannel = splitline[0]
    value = splitline[1]


    sql = 'INSERT INTO g2sc_calib_temp (subchannel, calib_value) '
    sql += "VALUES ("
    sql += "'" + subchannel + "', "
    sql += value + " "
    sql += ");"

    print sql
    if write_to_db:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()

conn.close()
