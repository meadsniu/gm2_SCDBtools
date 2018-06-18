"""
make_test_file.py

Python script to pull information from slow controls database and 
dump it into a text file.

M. Eads
Apr 2018
"""

import SCDButil

output_filename = 'kickersetv.txt'
outfile = open(output_filename, 'w')

# create the database object to handle the query
db = SCDButil.SCDButil(db='online')

# create the sql query
sql = 'SELECT * FROM g2sc_values '
sql += "WHERE channel = 'mscb282_DAC_P6' "
sql += "AND time >= '2018-04-09 9:00' "
sql += "AND time <= '2018-04-09 17:00' "

# execute the query
cur = db.execute_query(sql)
query_result = cur.fetchall()

# loop over the results, write to text file
names = {0:'kicker1setv', 1:'kicker2setv', 2:'kicker3setv'}

for entry in query_result:
    out = entry[3].isoformat() + ', '
    out += str(entry[2][0]) + ', ' + str(entry[2][1]) + ', ' + str(entry[2][2])
    out += '\n'

    print out
    outfile.write(out)







outfile.close()
