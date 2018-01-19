"""
RunDButil.py

Python utility class (RunDButil) to handle pulling data (like begin
and end run timestamps) from the runlog database.

M. Eads
Jan 2018
"""

import sys, time, datetime
import psycopg2

class RunDButil:
    """
    runDButil class is a utility class for accessing information in the 
    runlog database
    """

    def __init__(self, db='offline', calib = False):
        # initialize the database connection
        params = ""
        if db == 'online':
            params = 'dbname=gm2_online_prod user=gm2_reader host=localhost port=5433'
        elif db == 'offline':
            # if connecting from a Fermilab IP,. you don't need a password
            params = 'dbname=gm2_online_prod user=gm2_reader  host=ifdbprod.fnal.gov port=5452'
            # connecting from offsite requires a password, add it here
            #params = 'dbname=gm2_online_prod user=gm2_reader password=XXX  host=ifdbprod.fnal.gov port=5452'
        else:
            print 'Unknown database:', db
        self.conn = psycopg2.connect(params)

    def __del__(self):
        # close the database connection
        self.conn.close()

    def execute_query(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur

    def get_column(self, column, run):
        # generic method to get a particular column for a particluar run
        sql = "SELECT "
        sql += '"' + column + '"' + """ FROM runlog WHERE "Run number"="""
        sql += str(run)
        sql += " ;"
        #print sql

        cur = self.execute_query(sql)

        result = cur.fetchall()

        if len(result) == 0:
            print 'No', column, 'returned for run', run
            return
        elif len(result) > 1:
            print 'Multiple', column, 'results returned for run', run
            print result
            print "I'm confused and so will return nothing"
            return
        elif len(result) == 1:
            # only one result for this run, which is expected
            return result[0][0]

    def get_starttime(self, run):
        # method to return the run start time
        return self.get_column('Start time', run)
        
    def get_stoptime(self, run):
        # method to return the run start time
        return self.get_column('Stop time', run)

    def print_runinfo(self, run):
        # method to dump all the DB info for a particluar run
        sql = """SELECT * FROM runlog WHERE "Run number"="""
        sql += str(run)
        sql += ";"

        cur = self.execute_query(sql)
        result = cur.fetchall()
        #print result

        if len(result) == 0:
            print 'No results returned for run', run
        elif len(result) > 1:
            print 'Multiple results returned for run', run
            print "...I'm going to just dump eveything..."
            print result
        elif len(result) == 1:
            # only one result for the run is expected
            print '===== Results for Run', result[0][0], '====='
            print 'Time of entry:\t', result[0][1]
            print 'comment:\t', result[0][2]
            print 'Stop time:\t', result[0][3]
            print 'totalBytes:\t', result[0][4]
            print 'Start time:\t', result[0][5]
            print 'diskLevel:\t', result[0][6]
            print 'crew:\t\t', result[0][7]
            print 'dataDir:\t', result[0][8]
            print 'nEvents:\t', result[0][9]
            print 'nBytes:\t\t', result[0][10]
            print 'nFiles:\t\t', result[0][11]
            print 'quality:\t', result[0][12]

        return

        

if __name__ == '__main__':
    db = RunDButil()

    sql = """ SELECT * FROM runlog WHERE "Run number" = 8876; """
    cur = db.execute_query(sql)
    print cur.fetchall()
